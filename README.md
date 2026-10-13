<div align="center">

# SerpApi untuk Komunitas Developer Indonesia 🇮🇩

**Tutorial lokalasi + tool runnable** untuk melacak kata kunci SEO & memonitor
peringkat pencarian Google dari Indonesia — langsung dari SerpApi.

_Disusun untuk Developer Advocate (Indonesian) · Zainal Anwar Nugroho_

</div>

---

## Apa itu SerpApi, dalam 30 detik

SerpApi adalah API yang mengembalikan hasil mesin pencari (Google, Bing, dsb.)
sebagai JSON yang rapi. Satu `GET` request, satu respons — tanpa perlu scraping
sendiri, tanpa perlu jaga CAPTCHA, tanpa perlu urus perubahan layout halaman.
Pelanggannya termasuk Nvidia, Shopify, Perplexity, Adobe, dan Samsung.

Bagi developer & praktisi SEO Indonesia, satu use case paling terasa:

> **"Kata kunci bisnis saya ada di halaman berapa Google untuk pasar Indonesia?"**

SerpApi bisa menjawabnya, berulang, dan otomatis — cocok untuk dashboard,
cron job, atau laporan mingguan.

---

## Engine yang didukung

Tool ini mendukung 4 engine SerpApi, semuanya dengan default `gl=id&hl=id`:

| `--engine` | Mengembalikan | Contoh use case |
|---|---|---|
| `google` (default) | Peringkat web + PAA + related searches | Monitoring kata kunci |
| `google_news` | Berita (`news_results`) | Monitoring berita & sentiment |
| `google_maps` | Bisnis & tempat (`maps_results`) | Riset kompetitor lokal |
| `google_autocomplete` | Saran pencarian | Riset keyword & ide konten |

## 🇮🇩 Versi Bahasa Indonesia

### 1. Siapkan API key

1. Daftar di [serpapi.com](https://serpapi.com) — ada kuota gratis (100 search/bulan).
2. Salin API key Anda.
3. Simpan di lingkungan (jangan di-commit!):

```bash
export SERP_API_KEY="api_key_anda"
```

atau buat file `.env`:

```
SERP_API_KEY=api_key_anda
```

> 🔒 `SERP_API_KEY` ada di `.gitignore` (lewat `.env`). Jangan pernah menempel
> key di README, kode, atau commit.

### 2. Jalankan tool

Tool di repo ini **standalone — hanya pakai Python standard library**
(`urllib`, `json`). Tidak perlu `pip install` apa pun.

```bash
# Riset peringkat kata kunci (engine default: google)
python3 serp_idi_tracker.py --keyword "kafe terbaik bogor" --pages 5

# Monitoring berita
python3 serp_idi_tracker.py --engine google_news --keyword "gempa surabaya"

# Riset kompetitor lokal
python3 serp_idi_tracker.py --engine google_maps --keyword "kafe bogor"

# Riset saran pencarian
python3 serp_idi_tracker.py --engine google_autocomplete --keyword "cara membuat nasi goreng"
```

Contoh output (engine `google`):

```
== Ranking untuk "kafe terbaik bogor" (gl=id, hl=id) ==

 #  Judul                                                        Domain
 1  Kafe Terbaik di Bogor 2026 ...                             tripadvisor.co.id
 2  10 Kafe Hits di Bogor yang Wajib ...                        kompas.com
 3  Rekomendasi Kafe Estetik Bogor ...                           kaskus.id
 ...
```

### 3. Mode offline (tanpa API key)

Kalau Anda belum punya key, setiap engine punya sample di `samples/` sehingga
Anda tetap bisa melihat bentuk respons & cara membacanya:

```bash
python3 serp_idi_tracker.py --engine google_news --keyword "gempa surabaya" --offline
python3 serp_idi_tracker.py --engine google_maps --keyword "kafe bogor" --offline
```

### 4. Pelajari respons SerpApi

Bagian penting dalam respons, per engine:

| Engine | Field kunci | Berarti apa |
|---|---|---|
| `google` | `organic_results[]` | Hasil utama (pos 1–10) + `position`, `title`, `link`, `snippet` |
| `google` | `people_also_ask[]` | Pertanyaan terkait (bahan konten) |
| `google` | `related_searches[]` | Pencarian serupa (ide keyword) |
| `google_news` | `news_results[]` | `title`, `source`, `date` |
| `google_maps` | `maps_results[]` | `name`, `star_rating`, `num_reviews`, `address` |
| `google_autocomplete` | `autocomplete_results[]` | `suggestion` (saran pencarian) |

---

## 🇬🇧 English Version

### Quick start

```bash
export SERP_API_KEY="your_key"
python3 serp_idi_tracker.py --keyword "best coffee in bogor" --pages 5

# Or use another engine:
python3 serp_idi_tracker.py --engine google_news --keyword "surabaya earthquake"
python3 serp_idi_tracker.py --engine google_maps --keyword "coffee in bogor"
python3 serp_idi_tracker.py --engine google_autocomplete --keyword "how to make"


The tool calls `GET https://serpapi.com/search` with:

| param | value | why |
|---|---|---|
| `engine` | `google` | the search engine |
| `q` | your keyword | the query |
| `api_key` | your key | auth |
| `gl` | `id` | **locale = Indonesia** |
| `hl` | `id` | **language = Indonesian** |
| `google_domain` | `google.co.id` | local domain for more local results |

> The point of a localized tutorial: for an Indonesian audience, set
> `gl=id&hl=id&google_domain=google.co.id` so results reflect the Indonesian
> SERP, not `google.com`/US defaults.

Run without a key (offline demo) with `--offline`.

---

## Contoh Lokalisasi Dokumentasi

Repo ini menyertakan cuplikan dokumentasi SerpApi yang telah **diterjemahkan ke
Bahasa Indonesia** sebagai contoh gaya lokalasi yang kami gunakan:

| Docs | Engine |
|---|---|
| [`google-search-api-ID.md`](contoh_lokalisasi/google-search-api-ID.md) | `google` |
| [`google-news-api-ID.md`](contoh_lokalisasi/google-news-api-ID.md) | `google_news` |
| [`google-maps-api-ID.md`](contoh_lokalisasi/google-maps-api-ID.md) | `google_maps` |
| [`google-autocomplete-api-ID.md`](contoh_lokalisasi/google-autocomplete-api-ID.md) | `google_autocomplete` |

Pola lokalasi: terminologi teknis (`endpoint`, `GET`, `JSON`, `query parameter`)
dibiarkan dalam bahasa Inggris karena komunitas developer membacanya begitu;
narasi & contoh disesuaikan ke konteks Indonesia (kota, brand lokal, use case
lokal).

---

## Struktur repo

```
.
├── README.md                      # tutorial bilingual (ID + EN)
├── serp_idi_tracker.py            # tool runnable, stdlib-only, 4 engine
├── samples/                       # contoh respons SerpApi (mode offline)
│   ├── sample_google.json
│   ├── sample_google_news.json
│   ├── sample_google_maps.json
│   └── sample_google_autocomplete.json
├── contoh_lokalisasi/
│   ├── google-search-api-ID.md
│   ├── google-news-api-ID.md
│   ├── google-maps-api-ID.md
│   └── google-autocomplete-api-ID.md
├── .env.example                  # template environment
├── .gitignore
└── LICENSE                       # MIT
```

---

## Izin & kredit

- SerpApi & seluruh endpoint/doc referensinya milik [SerpApi](https://serpapi.com).
  Tutorial ini adalah karya lokalasi independen untuk tujuan edukasi.
- Isi folder `samples/` adalah cuplikan bentuk respons, bukan data produksi.
- Kode tool: MIT (lihat `LICENSE`).

---

## Ingin ikut membantu?

Kirim terjemahan docs SerpApi lain ke bahasa Indonesia, tambahan use case
lokal, atau perbaikan di tool ini — silakan buka issue / pull request.
Membangun dokumentasi lokal dalam bahasa ibu adalah kontribusi DevRel yang
paling berdampak untuk komunitas developer Indonesia.
