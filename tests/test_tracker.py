import contextlib
import io
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import urllib.error
import serp_idi_tracker as app

ROOT = Path(__file__).resolve().parents[1]

class TrackerTests(unittest.TestCase):
    def output(self, func, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = func(*args)
        return result, buf.getvalue()

    def test_stored_samples_use_expected_shapes(self):
        for engine in app.ENGINES:
            with self.subTest(engine=engine):
                data = app.load_sample(engine)
                self.assertIsInstance(data[app.RESULT_FIELDS[engine]], list)

    def test_four_offline_engines_do_not_fetch(self):
        with patch.object(app, 'fetch_serpapi') as fetch:
            for engine in app.ENGINES:
                status, output = self.output(app.main, ['--engine', engine, '--keyword', 'new-query-not-in-sample', '--offline'])
                self.assertEqual(status, 0)
                self.assertIn('OFFLINE', output)
                self.assertNotIn('new-query-not-in-sample', output)
            fetch.assert_not_called()

    def test_related_questions_are_rendered(self):
        data = {'organic_results': [], 'related_questions': [{'question':'Apa itu API?'}]}
        _, output = self.output(app.print_google, data, 'test', 'id', 'id')
        self.assertIn('Apa itu API?', output)

    def test_maps_zero_review_count_is_preserved(self):
        data = {'local_results':[{'title':'Contoh','rating':0,'reviews':0}]}
        _, output = self.output(app.print_maps, data, 'test', 'id', 'id')
        self.assertIn('ulasan=0', output)

    def test_autocomplete_values(self):
        _, output = self.output(app.print_autocomplete, {'suggestions':[{'value':'cara belajar'}]}, 'test','id','id')
        self.assertIn('cara belajar', output)

    def test_news_clusters(self):
        data = {'news_results':[{'stories':[{'title':'Judul','source':{'name':'Media'}}]}]}
        _, output = self.output(app.print_news, data, 'test', 'id', 'id')
        self.assertIn('Judul [Media', output)

    def test_empty_and_missing_fields_are_distinct(self):
        _, empty = self.output(app.print_google, {'organic_results':[]}, 'test','id','id')
        _, missing = self.output(app.print_google, {}, 'test','id','id')
        self.assertIn('kosong', empty)
        self.assertIn('tidak ada', missing)
        self.assertNotEqual(empty, missing)

    def test_error_payload_rejected(self):
        with self.assertRaises(app.ResponseError):
            app.validate_response({'error':'provider failure'}, 'google')

    def test_unfinished_or_failed_search_rejected(self):
        for status in ['Processing','Queued','Error']:
            with self.subTest(status=status), self.assertRaises(app.ResponseError):
                app.validate_response({'search_metadata':{'status':status}}, 'google')

    def test_invalid_shapes_rejected(self):
        for data in [[],None,{'search_metadata':[]},{'organic_results':{}},{'organic_results':['bad']}]:
            with self.subTest(data=data), self.assertRaises(app.ResponseError):
                app.validate_response(data, 'google')

    def test_engine_specific_parameters(self):
        google = app.build_params('google','test','dummy',page=2)
        self.assertEqual(google['start'],'10')
        self.assertEqual(google['google_domain'],'google.co.id')
        maps = app.build_params('google_maps','test','dummy')
        self.assertEqual(maps['type'],'search')
        self.assertNotIn('gl',maps)
        for engine in app.ENGINES[1:]:
            params = app.build_params(engine,'test','dummy')
            self.assertNotIn('start',params)
            self.assertNotIn('google_domain',params)

    def test_fetch_rejects_error_and_returns_nonzero_from_cli(self):
        response = io.BytesIO(b'{"error":"synthetic-provider-failure"}')
        err = io.StringIO()
        with patch.object(app,'load_key',return_value='DUMMY_SECRET'), patch.object(app.urllib.request,'urlopen',return_value=response), contextlib.redirect_stderr(err):
            status, output = self.output(app.main,['--keyword','test'])
        self.assertEqual(status,1)
        self.assertNotIn('DUMMY_SECRET',err.getvalue())
        self.assertNotIn('kosong',output)

    def test_http_error_does_not_leak_body_or_retry(self):
        for code in [401,403,429,500]:
            error = urllib.error.HTTPError('https://example.org?api_key=DUMMY_SECRET',code,'error',{},io.BytesIO(b'DUMMY_SECRET'))
            with patch.object(app.urllib.request,'urlopen',side_effect=error) as fetch:
                with self.assertRaises(app.ResponseError) as caught:
                    app.fetch_serpapi('google','test','DUMMY_SECRET','id','id','google.co.id',1)
                self.assertNotIn('DUMMY_SECRET',str(caught.exception))
                self.assertEqual(fetch.call_count,1)

    def test_bad_json_has_readable_error(self):
        with patch.object(app.urllib.request,'urlopen',return_value=io.BytesIO(b'not JSON')):
            with self.assertRaisesRegex(app.ResponseError,'JSON'):
                app.fetch_serpapi('google','test','dummy','id','id','google.co.id',1)

    def test_timeout_does_not_reveal_key(self):
        with patch.object(app.urllib.request,'urlopen',side_effect=TimeoutError('DUMMY_SECRET')):
            with self.assertRaises(app.ResponseError) as caught:
                app.fetch_serpapi('google','test','dummy','id','id','google.co.id',1)
            self.assertNotIn('DUMMY_SECRET',str(caught.exception))

    def test_cli_rejects_invalid_request_counts(self):
        for args in [['--pages','0'],['--pages','11'],['--pages','2','--offline'],['--pages','2','--engine','google_news']]:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                app.main(['--keyword','test']+args)

    def test_keyword_bounds(self):
        for query in ['  ','x'*301]:
            with self.assertRaises(ValueError):
                app.build_params('google',query,'dummy')

    def test_environment_alias(self):
        with patch.dict(app.os.environ, {'SERPAPI_API_KEY':'new','SERP_API_KEY':'old'}):
            self.assertEqual(app.load_key(),'new')

    def test_readme_links_and_fences(self):
        text=(ROOT/'README.md').read_text()
        self.assertEqual(sum(line.startswith('```') for line in text.splitlines())%2,0)
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if not link.startswith(('https:','http:','#')):
                self.assertTrue((ROOT/link).exists(),link)

    def test_guides_match_response_fields(self):
        for slug,field in [('google-search','organic_results'),('google-news','news_results'),('google-maps','local_results'),('google-autocomplete','suggestions')]:
            text=(ROOT/'contoh_lokalisasi'/(slug+'-api-ID.md')).read_text()
            self.assertIn('`'+field+'[]`',text)

if __name__ == '__main__':
    unittest.main()
