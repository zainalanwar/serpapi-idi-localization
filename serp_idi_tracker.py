#!/usr/bin/env python3
"""
serp_idi_tracker.py — Lacak & jelajahi hasil pencarian untuk pasar Indonesia.

Standalone: hanya Python standard library (urllib + json).
Tidak butuh `pip install`.

Support engine:
  google                 → hasil web + peringkat (default)
  google_news            → berita, parameter berita_date
  google_maps            → bisnis/tempat (maps_results)
  google_autocomplete    → saran pencarian (autocomplete_results)

Mode:
  live     → panggil SerpApi (butuh SERP_API_KEY)
  offline  → baca samples/sample_<engine>.json (tanpa API key)

Contoh:
  export SERP_API_KEY="..."
  python3 serp_idi_tracker.py --keyword "kafe terbaik bogor" --pages 5
  python3 serp_idi_tracker.py --engine google_news --keyword "gempa surabaya"
  python3 serp_idi_tracker.py --engine google_maps --keyword "kafe bogor" --offline
  python3 serp_idi_tracker.py --engine google_autocomplete --keyword "cara membuat" --offline
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_ENDPOINT = "https://serpapi.com/search"
DEFAULT_GL = "id"          # locale: Indonesia
DEFAULT_HL = "id"          # language: Indonesian
DEFAULT_DOMAIN = "google.co.id"

ENGINES = ("google", "google_news", "google_maps", "google_autocomplete")


def load_key():
    """Ambil SERP_API_KEY dari environment, kalau belum ada dari file .env."""
    if os.environ.get("SERP_API_KEY"):
        return os.environ["SERP_API_KEY"]
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        for line in open(env_path, encoding="utf-8"):
            line = line.strip()
            if line.startswith("SERP_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


def fetch_serpapi(engine, keyword, api_key, gl, hl, domain, page):
    """Jalankan satu GET request ke SerpApi dan kembalikan JSON."""
    params = {
        "engine": engine,
        "q": keyword,
        "api_key": api_key,
        "gl": gl,
        "hl": hl,
        "google_domain": domain,
        "start": str((page - 1) * 10),
    }
    if engine == "google_news":
        params.pop("google_domain", None)
        params.pop("start", None)
    url = API_ENDPOINT + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "serp-id-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_sample(engine):
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "samples", f"sample_{engine}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _domain(link):
    try:
        return urllib.parse.urlsplit(link).netloc
    except Exception:
        return link or ""


def print_google(data, keyword, gl, hl):
    organic = data.get("organic_results", [])
    print(f'== Ranking untuk "{keyword}" (gl={gl}, hl={hl}) ==\n')
    if not organic:
        print("(tidak ada organic_results — periksa keyword atau mode offline)")
    width_title = 52
    print(f" {'#':>2}  {'Judul':<{width_title}} {'Domain'}")
    print(f" {'-'*2}  {'-'*width_title}  {'-'*20}")
    for r in organic[:10]:
        pos = r.get("position", "?")
        title = (r.get("title") or "")[:width_title]
        print(f" {pos:>2}  {title:<{width_title}} {_domain(r.get('link'))}")
    paa = data.get("people_also_ask", [])
    if paa:
        print("\n== People Also Ask ==")
        for q in paa[:5]:
            print(f"  • {q.get('question')}")
    rel = data.get("related_searches", [])
    if rel:
        print("\n== Related Searches ==")
        for q in rel[:5]:
            print(f"  • {q.get('query')}")


def print_news(data, keyword, gl, hl):
    news = data.get("news_results", data.get("news", []))
    print(f'== Berita untuk "{keyword}" (gl={gl}, hl={hl}) ==\n')
    if not news:
        print("(tidak ada news_results — periksa keyword atau mode offline)")
    for r in news[:10]:
        title = r.get("title") or r.get("name") or ""
        source = r.get("source") or ""
        if isinstance(source, dict):
            source = source.get("name", "")
        date = r.get("date") or ""
        print(f"  • {title}")
        if source or date:
            print(f"    [{source} · {date}]")


def print_maps(data, keyword, gl, hl):
    places = data.get("local_results", data.get("maps_results", []))
    print(f'== Tempat/Bisnis untuk "{keyword}" (gl={gl}, hl={hl}) ==\n')
    if not places:
        print("(tidak ada local_results — periksa keyword atau mode offline)")
    for p in places[:10]:
        name = p.get("title") or p.get("name") or ""
        stars = p.get("rating") or p.get("star_rating")
        count = p.get("reviews") or p.get("num_reviews")
        ptype = p.get("type") or ""
        rating = f" ({stars}★, {count} ulasan)" if stars else ""
        typetxt = f" — {ptype}" if ptype else ""
        print(f"  • {name}{rating}{typetxt}")
        if p.get("address"):
            print(f"    {p['address']}")


def print_autocomplete(data, keyword, gl, hl):
    sugg = data.get("suggestions", data.get("autocomplete_results", []))
    print(f'== Saran Autocomplete untuk "{keyword}" (gl={gl}, hl={hl}) ==\n')
    if not sugg:
        print("(tidak ada suggestions — periksa keyword atau mode offline)")
    for s in sugg[:15]:
        if isinstance(s, dict):
            text = s.get("value", s.get("suggestion", ""))
        else:
            text = str(s)
        print(f"  • {text}")


PRINTERS = {
    "google": print_google,
    "google_news": print_news,
    "google_maps": print_maps,
    "google_autocomplete": print_autocomplete,
}


def main():
    ap = argparse.ArgumentParser(description="Lacak hasil pencarian Indonesia via SerpApi")
    ap.add_argument("--keyword", required=True, help="Kata kunci yang ingin ditelusuri")
    ap.add_argument("--engine", choices=ENGINES, default="google",
                    help="Engine SerpApi (default: google)")
    ap.add_argument("--pages", type=int, default=1, help="Jumlah halaman (engine google, default 1)")
    ap.add_argument("--gl", default=DEFAULT_GL, help="Country code (default: id)")
    ap.add_argument("--hl", default=DEFAULT_HL, help="Language code (default: id)")
    ap.add_argument("--domain", default=DEFAULT_DOMAIN, help="Google domain (default: google.co.id)")
    ap.add_argument("--offline", action="store_true", help="Pakai samples/, tanpa API key")
    args = ap.parse_args()

    printer = PRINTERS[args.engine]

    if args.offline:
        data = load_sample(args.engine)
        printer(data, args.keyword, args.gl, args.hl)
        print(f"\n[mode offline: sample_{args.engine}.json]")
        return 0

    api_key = load_key()
    if not api_key:
        print("Tidak ada SERP_API_KEY. Set lewat environment atau file .env, atau jalankan --offline.", file=sys.stderr)
        return 1

    pages = args.pages if args.engine == "google" else 1
    for page in range(1, pages + 1):
        print(f"\n--- Halaman {page} ---\n")
        try:
            data = fetch_serpapi(args.engine, args.keyword, api_key, args.gl, args.hl, args.domain, page)
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Gagal memanggil SerpApi: {e}", file=sys.stderr)
            return 1
        printer(data, args.keyword, args.gl, args.hl)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
