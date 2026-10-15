#!/usr/bin/env python3
"""Explore SerpApi responses with Indonesian examples. Python standard library only.

AI-assisted educational sample. Offline replay is not a live request or a
measurement of ranking changes. See VERIFICATION.md for validation limits.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

API_ENDPOINT = "https://serpapi.com/search"
ENGINES = ("google", "google_news", "google_maps", "google_autocomplete")
RESULT_FIELDS = dict(zip(ENGINES, ("organic_results", "news_results", "local_results", "suggestions")))


class ResponseError(ValueError):
    """The provider response cannot be treated as completed search data."""


def load_key():
    key = os.environ.get("SERPAPI_API_KEY") or os.environ.get("SERP_API_KEY")
    if key:
        return key.strip()
    path = Path(__file__).resolve().parent / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            name, sep, value = line.strip().partition("=")
            if sep and name.strip() in ("SERPAPI_API_KEY", "SERP_API_KEY"):
                value = value.strip().strip("\"'")
                if value:
                    return value
    return None


def build_params(engine, keyword, api_key, gl="id", hl="id", domain="google.co.id", page=1):
    if engine not in ENGINES:
        raise ValueError("Unsupported engine.")
    if not keyword.strip() or len(keyword) > 300:
        raise ValueError("Use a keyword between 1 and 300 characters.")
    if not 1 <= page <= 10:
        raise ValueError("Page must be between 1 and 10.")
    params = {"engine": engine, "q": keyword.strip(), "api_key": api_key, "hl": hl}
    if engine != "google_maps":
        params["gl"] = gl
    if engine == "google":
        params.update(google_domain=domain, start=str((page - 1) * 10))
    if engine == "google_maps":
        params["type"] = "search"
    return params


def validate_response(data, engine):
    if not isinstance(data, dict):
        raise ResponseError("Expected a JSON object; inspect the response format.")
    if data.get("error"):
        raise ResponseError("SerpApi returned an error. Check the request and account; no results were analyzed.")
    metadata = data.get("search_metadata", {})
    if not isinstance(metadata, dict):
        raise ResponseError("Invalid search_metadata object.")
    if metadata.get("status") in ("Processing", "Queued", "Error"):
        raise ResponseError("Search is not successfully completed. Inspect its status before retrying.")
    field = RESULT_FIELDS[engine]
    if field in data and not isinstance(data[field], list):
        raise ResponseError("Expected an array in " + field + ".")
    if any(not isinstance(row, dict) for row in data.get(field, [])):
        raise ResponseError("Expected result objects in " + field + ".")
    return data


def fetch_serpapi(engine, keyword, api_key, gl, hl, domain, page):
    params = build_params(engine, keyword, api_key, gl, hl, domain, page)
    req = urllib.request.Request(API_ENDPOINT + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": "serpapi-indonesian-learning-sample/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        messages = {401: "Authentication failed; check your API key.",
                    403: "Access denied; check account permissions.",
                    429: "Quota or throughput limit; inspect your account before retrying."}
        raise ResponseError(messages.get(error.code, "HTTP " + str(error.code) + "; retry only after checking the service.")) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ResponseError("Network request failed; check connectivity. No automatic retry was made.") from None
    except (json.JSONDecodeError, UnicodeError):
        raise ResponseError("The response was not valid UTF-8 JSON.") from None
    return validate_response(data, engine)


def load_sample(engine):
    path = Path(__file__).resolve().parent / "samples" / ("sample_" + engine + ".json")
    return validate_response(json.loads(path.read_text(encoding="utf-8")), engine)


def rows(data, engine):
    field = RESULT_FIELDS[engine]
    if field not in data:
        print("Field " + field + " tidak ada pada respons; periksa bentuk SERP dan respons lengkap.")
    elif not data[field]:
        print(field + " kosong pada respons ini.")
    return data.get(field, [])


def print_google(data, keyword, gl, hl):
    print(f'Hasil web untuk "{keyword}" (gl={gl}, hl={hl})')
    for result in rows(data, "google")[:10]:
        domain = urllib.parse.urlsplit(result.get("link") or "").netloc
        print(f"  {result.get('position', '?')}. {result.get('title', '')} | {domain}")
    questions = data.get("related_questions", [])
    if questions:
        print("\nPertanyaan terkait")
        for question in questions[:5]:
            print("  - " + question.get("question", ""))
    related = data.get("related_searches", [])
    if related:
        print("\nPencarian terkait")
        for result in related[:5]:
            print("  - " + result.get("query", ""))


def print_news(data, keyword, gl, hl):
    print(f'Berita untuk "{keyword}" (gl={gl}, hl={hl})')
    for result in rows(data, "google_news")[:10]:
        # Google News can return a cluster with nested stories.
        stories = result.get("stories") or [result]
        for story in stories:
            source = story.get("source") or ""
            if isinstance(source, dict):
                source = source.get("name", "")
            print(f"  - {story.get('title', '')} [{source} | {story.get('date', '')}]")


def print_maps(data, keyword, gl, hl):
    print(f'Tempat untuk "{keyword}" (hl={hl}; lokasi mengikuti query)')
    for place in rows(data, "google_maps")[:10]:
        print(f"  - {place.get('title', '')} | rating={place.get('rating', 'n/a')} | ulasan={place.get('reviews', 'n/a')}")
        if place.get("address"):
            print("    " + place["address"])


def print_autocomplete(data, keyword, gl, hl):
    print(f'Saran untuk "{keyword}" (gl={gl}, hl={hl})')
    for suggestion in rows(data, "google_autocomplete")[:15]:
        print("  - " + suggestion.get("value", ""))


PRINTERS = dict(zip(ENGINES, (print_google, print_news, print_maps, print_autocomplete)))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Jelajahi respons SerpApi untuk contoh Indonesia")
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--engine", choices=ENGINES, default="google")
    parser.add_argument("--pages", type=int, default=1, help="Google only, 1-10 requests; default 1")
    parser.add_argument("--gl", default="id", help="Country for Google, News and Autocomplete")
    parser.add_argument("--hl", default="id", help="Search interface language")
    parser.add_argument("--domain", default="google.co.id", help="Google Search only")
    parser.add_argument("--offline", action="store_true", help="Replay one stored sample; no request")
    args = parser.parse_args(argv)
    if not args.keyword.strip() or len(args.keyword) > 300:
        parser.error("Keyword harus berisi 1-300 karakter.")
    if not 1 <= args.pages <= 10:
        parser.error("--pages harus 1-10.")
    if args.pages != 1 and (args.engine != "google" or args.offline):
        parser.error("--pages > 1 hanya tersedia untuk Google live; offline memutar satu sample.")
    try:
        if args.offline:
            data = load_sample(args.engine)
            original = data.get("search_parameters", {})
            print("OFFLINE: replay sample tersimpan; --keyword tidak menjalankan pencarian baru.")
            PRINTERS[args.engine](data, original.get("q", "sample"), original.get("gl", args.gl), original.get("hl", args.hl))
            return 0
        key = load_key()
        if not key:
            print("Set SERPAPI_API_KEY secara lokal atau gunakan --offline.", file=sys.stderr)
            return 1
        for page in range(1, args.pages + 1):
            print(f"\nHalaman {page}; maksimal {args.pages} request, tanpa retry otomatis.")
            data = fetch_serpapi(args.engine, args.keyword, key, args.gl, args.hl, args.domain, page)
            PRINTERS[args.engine](data, args.keyword, args.gl, args.hl)
        return 0
    except (ResponseError, OSError, json.JSONDecodeError) as error:
        # Do not emit raw HTTP bodies or URLs that might contain the API key.
        message = str(error) if isinstance(error, ResponseError) else "Sample tidak dapat dibaca; periksa file JSON lokal."
        print(message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
