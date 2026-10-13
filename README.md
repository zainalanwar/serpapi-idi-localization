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
python3 serp_idi_tracker.py --keyword "kafe terbaik bogor" --pages 5
```

Contoh output:

```
== Ranking untuk "kafe terbaik bogor" (gl=id, hl=id) ==

 #  Judul                                                        Domain
 1  Kafe Terbaik di Bogor 2026 ...                             tripadvisor.co.id
 2  10 Kafe Hits di Bogor yang Wajib ...                        kompas.com
 3  Rekomendasi Kafe Estetik Bogor ...                           kaskus.id
 ...
```

### 3. Mode offline (tanpa API key)

Kalau Anda belum punya key, tool otomatis fallback ke `sample_response.json`
sehingga Anda tetap bisa melihat bentuk respons & cara membacanya:

```bash
python3 serp_idi_tracker.py --keyword "kafe terbaik bogor" --offline
```

### 4. Pelajari respons SerpApi

Bagian penting dalam respons Google Search:

| Field | Berarti apa |
|---|---|
| `organic_results[]` | Hasil utama (pos 1–10). Ini yang Anda monitor |
| `organic_results[].position` | Peringkat |
| `organic_results[].title` / `link` / `snippet` | Judul, URL, deskripsi |
| `people_also_ask[]` | Pertanyaan terkait (bahan konten) |
| `related_searches[]` | Pencarian serupa (ide keyword) |
| `search_information` | Estimasi jumlah hasil, durasi query |

---

## 🇬🇧 English Version

### Quick start

```bash
export SERP_API_KEY="your_key"
python3 serp_idi_tracker.py --keyword "best coffee in bogor" --pages 5
```

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

→ lihat [`contoh_lokalisasi/google-search-api-ID.md`](contoh_lokalisasi/google-search-api-ID.md)

Pola lokalasi: terminologi teknis (`endpoint`, `GET`, `JSON`, `query parameter`)
dibiarkan dalam bahasa Inggris karena komunitas developer membacanya begitu;
narasi & contoh disesuaikan ke konteks Indonesia (kota, brand lokal, use case
lokal).

---

## Struktur repo

```
.
├── README.md                      # tutorial bilingual (ID + EN)
├── serp_idi_tracker.py            # tool runnable, stdlib-only
├── sample_response.json          # contoh respons SerpApi (mode offline)
├── contoh_lokalisasi/
│   └── google-search-api-ID.md   # cuplikan docs SerpApi → Indonesia
├── .env.example                  # template environment
├── .gitignore
└── LICENSE                       # MIT
```

---

## Izin & kredit

- SerpApi & seluruh endpoint/doc referensinya milik [SerpApi](https://serpapi.com).
  Tutorial ini adalah karya lokalasi independen untuk tujuan edukasi.
- `sample_response.json` adalah cuplikan bentuk respons, bukan data produksi.
- Kode tool: MIT (lihat `LICENSE`).

---

## Ingin ikut membantu?

Kirim terjemahan docs SerpApi lain ke bahasa Indonesia, tambahan use case
lokal, atau perbaikan di tool ini — silakan buka issue / pull request.
Membangun dokumentasi lokal dalam bahasa ibu adalah kontribusi DevRel yang
paling berdampak untuk komunitas developer Indonesia.
