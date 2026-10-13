# Google Maps API — Panduan Lokalisasi (Bahasa Indonesia)

> Cuplikan dokumentasi SerpApi yang telah diterjemahkan ke Bahasa Indonesia
> sebagai contoh gaya lokalasi untuk komunitas developer.
>
> **Catatan lokalasi:** istilah teknis (`endpoint`, `GET`, `JSON`,
> `maps_results`) **dibiarkan dalam bahasa Inggris**; narasi & use case
> disesuaikan ke konteks Indonesia.

## Apa yang dilakukan `engine=google_maps`

Endpoint `GET https://serpapi.com/search` dengan `engine=google_maps`
mengembalikan data **tempat & bisnis** dari Google Maps — nama, rating,
jumlah ulasan, dan alamat. Cocok untuk research kompetitor lokal,
pilihan lokasi, atau agregasi data usaha.

## Paramter penting

| Parameter | Wajib | Contoh | Fungsi |
|---|---|---|---|
| `q` | **Ya** | `kafe bogor` | Pencarian tempat/bisnis |
| `engine` | — | `google_maps` | Pilih mesin Maps |
| `gl` | Tidak | `id` | **Negara = Indonesia** |
| `hl` | Tidak | `id` | **Bahasa = Indonesia** |

### Contoh request untuk pasar Indonesia

```bash
curl --get "https://serpapi.com/search" \
  --data-urlencode "engine=google_maps" \
  --data-urlencode "q=kafe bogor" \
  --data-urlencode "gl=id" \
  --data-urlencode "hl=id" \
  --data-urlencode "api_key=API_KEY_ANDA"
```

> **Kunci lokalasi:** untuk research kompetitor Indonesia, set
> `gl=id&hl=id` dan gunakan `q` dengan nama kota/lokasi (mis. `kafe bogor`).

## Membaca respons

- **`maps_results[]`** — daftar tempat/bisnis
  - `name` — nama usaha
  - `star_rating` — rating (skala 1–5)
  - `num_reviews` — jumlah ulasan
  - `address` — alamat

Tool runnable: [`../serp_idi_tracker.py`](../serp_idi_tracker.py) dengan
`--engine google_maps`.

---
*Terjemahan independen untuk tujuan edukasi. Referensi asli:
[SerpApi Google Maps API](https://serpapi.com/google-maps-api).*
