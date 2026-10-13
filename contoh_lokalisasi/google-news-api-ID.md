# Google News API — Panduan Lokalisasi (Bahasa Indonesia)

> Cuplikan dokumentasi SerpApi yang telah diterjemahkan ke Bahasa Indonesia
> sebagai contoh gaya lokalasi untuk komunitas developer.
>
> **Catatan lokalasi:** istilah teknis (`endpoint`, `GET`, `JSON`,
> `news_results`) **dibiarkan dalam bahasa Inggris**; narasi & use case
> disesuaikan ke konteks Indonesia.

## Apa yang dilakukan `engine=google_news`

Endpoint `GET https://serpapi.com/search` dengan `engine=google_news`
mengembalikan hasil **Google News** dalam bentuk `JSON` yang terstruktur —
judul, sumber, dan waktu publikasi. Cocok untuk monitoring berita,
sentiment tracking, dan agregasi konten berita lokal.

## Paramter penting

| Parameter | Wajib | Contoh | Fungsi |
|---|---|---|---|
| `q` | **Ya** | `gempa surabaya` | Kata kunci berita |
| `engine` | — | `google_news` | Pilih mesin berita |
| `gl` | Tidak | `id` | **Negara = Indonesia** |
| `hl` | Tidak | `id` | **Bahasa = Indonesia** |

### Contoh request untuk pasar Indonesia

```bash
curl --get "https://serpapi.com/search" \
  --data-urlencode "engine=google_news" \
  --data-urlencode "q=gempa surabaya" \
  --data-urlencode "gl=id" \
  --data-urlencode "hl=id" \
  --data-urlencode "api_key=API_KEY_ANDA"
```

> **Kunci lokalasi:** set `gl=id&hl=id` agar berita yang dikembalikan relevan
> dengan pasar Indonesia, bukan default `us`.

## Membaca respons

- **`news_results[]`** — daftar berita
  - `title` — judul berita
  - `source` — media yang memuat
  - `date` — waktu publikasi

Tool runnable: [`../serp_idi_tracker.py`](../serp_idi_tracker.py) dengan
`--engine google_news`.

---
*Terjemahan independen untuk tujuan edukasi. Referensi asli:
[SerpApi Google News API](https://serpapi.com/google-news-api).*
