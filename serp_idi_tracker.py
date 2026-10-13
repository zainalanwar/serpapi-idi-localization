#!/usr/bin/env python3
"""
serp_idi_tracker.py — Lacak peringkat kata kunci untuk pasar Indonesia.

Standalone: hanya Python standard library (urllib + json).
Tidak butuh `pip install`.

Mode:
  live     → panggil SerpApi (butuh SERP_API_KEY)
  offline  → baca sample_response.json (tanpa API key)

Contoh:
  export SERP_API_KEY="..."
  python3 serp_idi_tracker.py --keyword "kafe terbaik bogor" --pages 5
  python3 serp_idi_tracker.py --keyword "kafe terbaik bogor" --offline
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

API_ENDPOINT = "https://serpapi.com/search"
DEFAULT_GL = "id"        # locale: Indonesia
DEFAULT_HL = "id"        # language: Indonesian
DEFAULT_DOMAIN = "google.co.id"


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


def fetch_serpapi(keyword, api_key, gl, hl, domain, page):
    """Jalankan satu GET request ke SerpApi dan kembalikan JSON."""
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": api_key,
        "gl": gl,
        "hl": hl,
        "google_domain": domain,
        "start": str((page - 1) * 10),
    }
    url = API_ENDPOINT + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "serp-id-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_sample():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_response.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def print_ranking(data, keyword, gl, hl):
    organic = data.get("organic_results", [])
    print(f'== Ranking untuk "{keyword}" (gl={gl}, hl={hl}) ==\n')
    if not organic:
        print("(tidak ada organic_results — periksa keyword atau mode offline)")
    width_title = 52
    print(f" {'#':>2}  {'Judul':<{width_title}} {'Domain'}")
    print(f" {'-'*2}  {'-'*width_title}  {'-'*20}")
    for r in organic[:10]:
        pos = r.get("position", "?")
        title = r.get("title", "")[:width_title]
        try:
            domain = urllib.parse.urlsplit(r.get("link", "")).netloc
        except Exception:
            domain = r.get("link", "")
        print(f" {pos:>2}  {title:<{width_title}} {domain}")
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


def main():
    ap = argparse.ArgumentParser(description="Lacak peringkat kata kunci Indonesia via SerpApi")
    ap.add_argument("--keyword", required=True, help="Kata kunci yang ingin ditelusuri")
    ap.add_argument("--pages", type=int, default=1, help="Jumlah halaman hasil (default 1)")
    ap.add_argument("--gl", default=DEFAULT_GL, help="Country code (default: id)")
    ap.add_argument("--hl", default=DEFAULT_HL, help="Language code (default: id)")
    ap.add_argument("--domain", default=DEFAULT_DOMAIN, help="Google domain (default: google.co.id)")
    ap.add_argument("--offline", action="store_true", help="Pakai sample_response.json, tanpa API key")
    args = ap.parse_args()

    if args.offline:
        data = load_sample()
        print_ranking(data, args.keyword, args.gl, args.hl)
        print("\n[mode offline: menampilkan sample response]")
        return 0

    api_key = load_key()
    if not api_key:
        print("Tidak ada SERP_API_KEY. Set lewat environment atau file .env, atau jalankan --offline.", file=sys.stderr)
        return 1

    for page in range(1, args.pages + 1):
        print(f"\n--- Halaman {page} ---\n")
        try:
            data = fetch_serpapi(args.keyword, api_key, args.gl, args.hl, args.domain, page)
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code}: {e.read().decode('utf-8','replace')}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Gagal memanggil SerpApi: {e}", file=sys.stderr)
            return 1
        print_ranking(data, args.keyword, args.gl, args.hl)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
