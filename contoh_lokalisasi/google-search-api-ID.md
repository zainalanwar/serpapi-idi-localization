# Google Search API — Panduan Lokalisasi (Bahasa Indonesia)

> Cuplikan dokumentasi SerpApi yang telah diterjemahkan ke Bahasa Indonesia
> sebagai contoh gaya lokalasi untuk komunitas developer.
>
> **Catatan lokalasi:** istilah teknis (`endpoint`, `GET`, `JSON`,
> `query parameter`, `api_key`, `organic_results`) **dibiarkan dalam bahasa
> Inggris** karena komunitas developer membacanya dalam bentuk asli. Yang
> diterjemahkan: narasi, langkah, dan contoh use case.

## Apa yang dilakukan endpoint `search`

Endpoint `GET https://serpapi.com/search` mengembalikan hasil pencarian mesin
mencari (default: Google) dalam bentuk `JSON` yang terstruktur. Satu request,
satu respons — tidak perlu scraping, tidak perlu mengelola CAPTCHA.

## Paramter wajib

| Parameter | Wajib | Fungsi |
|---|---|---|
| `api_key` | **Ya** | API key SerpApi Anda |
| `q` | **Ya** | Kata kunci pencarian |

## Paramter penting untuk pasar Indonesia

| Parameter | Contoh | Berfungsi untuk |
|---|---|---|
| `engine` | `google` | Pilih mesin pencari |
| `gl` | `id` | **Lokasi (locale) = Indonesia** |
| `hl` | `id` | **Bahasa hasil = Bahasa Indonesia** |
| `google_domain` | `google.co.id` | Domain Google lokal, biar hasil lebih sesuai pasar lokal |
| `start` | `0`, `10` | Paginasi hasil |

### Contoh request untuk pasar Indonesia

```bash
curl --get "https://serpapi.com/search" \
  --data-urlencode "engine=google" \
  --data-urlencode "q=kafe terbaik bogor" \
  --data-urlencode "gl=id" \
  --data-urlencode "hl=id" \
  --data-urlencode "google_domain=google.co.id" \
  --data-urlencode "api_key=API_KEY_ANDA"
```

> **Kunci lokalasi:** untuk audiens Indonesia, set `gl=id&hl=id&google_domain=google.co.id`.
> Tanpa paramter ini, hasil default-nya mengikuti `google.com`/US — dan peringkat
> kata kunci untuk pasar Indonesia tidak akurat.

## Membaca respons

Respons berisi beberapa bagian:

- **`organic_results[]`** — hasil utama (pos 1–10).
  - `position` — peringkat
  - `title`, `link`, `snippet` — judul, URL, deskripsi
- **`people_also_ask[]`** — pertanyaan terkait (bahan ide konten)
- **`related_searches[]`** — pencarian serupa (ekspansi keyword)
- **`search_information`** — estimasi jumlah hasil & durasi query

## Use case lokal

Lacak peringkat kata kunci bisnis Anda untuk pasar Indonesia, berulang dan
otomatis — untuk dashboard, cron mingguan, atau laporan. Tool runnable-nya ada
di [`../serp_idi_tracker.py`](../serp_idi_tracker.py).

---
*Terjemahan independen untuk tujuan edukasi. Referensi asli:
[SerpApi Google Search API](https://serpapi.com/search-api).*
