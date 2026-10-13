# Google Autocomplete API — Panduan Lokalisasi (Bahasa Indonesia)

> Cuplikan dokumentasi SerpApi yang telah diterjemahkan ke Bahasa Indonesia
> sebagai contoh gaya lokalasi untuk komunitas developer.
>
> **Catatan lokalasi:** istilah teknis (`endpoint`, `GET`, `JSON`,
> `autocomplete_results`) **dibiarkan dalam bahasa Inggris**; narasi & use case
> disesuaikan ke konteks Indonesia.

## Apa yang dilakukan `engine=google_autocomplete`

Endpoint `GET https://serpapi.com/search` dengan `engine=google_autocomplete`
mengembalikan **saran pencarian (suggestions)** yang muncul saat mengetik di
kotak pencarian Google. Ini adalah data perilaku pencarian nyata — sangat
berguna untuk riset keyword, ide konten, dan memahami apa yang sebenarnya
dicari orang.

## Paramter penting

| Parameter | Wajib | Contoh | Fungsi |
|---|---|---|---|
| `q` | **Ya** | `cara membuat` | Awalan kata kunci |
| `engine` | — | `google_autocomplete` | Pilih mesin autocomplete |
| `gl` | Tidak | `id` | **Negara = Indonesia** |
| `hl` | Tidak | `id` | **Bahasa = Indonesia** |

### Contoh request untuk pasar Indonesia

```bash
curl --get "https://serpapi.com/search" \
  --data-urlencode "engine=google_autocomplete" \
  --data-urlencode "q=cara membuat nasi goreng" \
  --data-urlencode "gl=id" \
  --data-urlencode "hl=id" \
  --data-urlencode "api_key=API_KEY_ANDA"
```

> **Kunci lokalasi:** set `gl=id&hl=id` agar saran yang dikembalikan
> mencerminkan perilaku pencarian berbahasa Indonesia, bukan global.

## Membaca respons

- **`autocomplete_results[]`** — daftar saran
  - `suggestion` — saran pencarian lengkap

Use case populer: kumpulkan saran untuk banyak awalan kata kunci, gabungkan,
dan jadikan *keyword pool* untuk konten atau SEO.

Tool runnable: [`../serp_idi_tracker.py`](../serp_idi_tracker.py) dengan
`--engine google_autocomplete`.

---
*Terjemahan independen untuk tujuan edukasi. Referensi asli:
[SerpApi Google Autocomplete API](https://serpapi.com/google-autocomplete-api).*
