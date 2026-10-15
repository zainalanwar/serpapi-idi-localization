# Belajar SerpApi untuk pengguna Indonesia

Contoh Python dan tutorial Indonesia untuk membaca hasil Google Search, News,
Maps, dan Autocomplete. Mulai dengan satu pertanyaan: data apa yang membantu
pengguna menyelesaikan tugasnya, dan bagaimana membaca responsnya dengan benar?

Disiapkan oleh Zainal Anwar Nugroho untuk aplikasi Indonesian Developer Advocate.
Kode dan dokumentasi dikembangkan dengan bantuan AI. Ini proyek edukasi independen,
bukan dokumentasi resmi SerpApi. Batas pengujian dicatat di [VERIFICATION.md](VERIFICATION.md).

## Coba tanpa akun

Python 3.9 atau lebih baru; hanya standard library. Tidak perlu instalasi package.

```bash
git clone https://github.com/zainalanwar/serpapi-idi-localization.git
cd serpapi-idi-localization
python3 serp_idi_tracker.py --engine google_maps --keyword "kafe bogor" --offline
```

Output menampilkan nama usaha, rating, jumlah ulasan dan alamat dari sample
tersimpan. Mode offline tidak mencari keyword baru: label query diambil dari
sample asli. Rating bukan ukuran kualitas yang objektif dan tidak menjelaskan
penyebab ulasan negatif. Untuk analisis isi ulasan diperlukan data lain, misalnya
Google Maps Reviews API, serta pemeriksaan konteks.

## Lakukan satu request live

Sediakan API key akun Anda. Lihat [paket resmi](https://serpapi.com/pricing) untuk
kuota terkini. Request live dapat memakai kuota; perintah default hanya satu request.

```bash
export SERPAPI_API_KEY="your_key"
python3 serp_idi_tracker.py --keyword "cara riset keyword"
```

Alternatif: salin `.env.example` menjadi `.env` di root repo dan isi sendiri.
`SERP_API_KEY` tetap diterima untuk kompatibilitas versi lama. Jangan membagikan
file `.env`, URL yang memuat key, atau screenshot credential.

## Pilih data yang sesuai tugas

| Engine | Field respons | Contoh tugas |
| --- | --- | --- |
| `google` | `organic_results`, `related_questions`, `related_searches` | Membaca jenis halaman dan pertanyaan yang muncul |
| `google_news` | `news_results` dan kadang `stories` di dalamnya | Membaca judul, sumber dan waktu berita |
| `google_maps` | `local_results` | Mengidentifikasi tempat yang perlu diteliti |
| `google_autocomplete` | `suggestions` | Mengumpulkan hipotesis ide keyword |

```bash
python3 serp_idi_tracker.py --engine google_news --keyword "gempa surabaya" --offline
python3 serp_idi_tracker.py --engine google_autocomplete --keyword "cara membuat" --offline
```

Untuk request live, hapus `--offline`. Pada Google Search, `--pages 2` membuat
hingga dua request. Tool ini menampilkan snapshot SERP; belum menyimpan riwayat,
menjadwalkan pencarian, atau menghitung perubahan peringkat domain.

## Memahami lokasi dan bahasa

Google Search, News, dan Autocomplete memakai `gl=id` dan `hl=id` secara default.
Google Search juga memakai `google_domain=google.co.id`. `gl` memilih negara
pencarian; `hl` mengatur bahasa pencarian, bukan jaminan semua halaman berbahasa
Indonesia. Untuk pembatasan bahasa hasil Google Search, pelajari `lr` pada
dokumentasi resmi. Lokasi presisi, perangkat, waktu dan fitur SERP juga berpengaruh.

Pada Maps, contoh memakai `type=search`, `hl=id` dan nama kota dalam `q`.
Untuk pencarian geografis yang lebih terkontrol, pelajari parameter `ll` di
dokumentasi Maps. Parameter antar-engine tidak selalu sama.

## Tutorial Indonesia

- [Google Search](contoh_lokalisasi/google-search-api-ID.md)
- [Google News](contoh_lokalisasi/google-news-api-ID.md)
- [Google Maps](contoh_lokalisasi/google-maps-api-ID.md)
- [Google Autocomplete](contoh_lokalisasi/google-autocomplete-api-ID.md)
- [Latihan membaca respons dan troubleshooting](docs/tutorial-id.md)

## English quick start

This learning sample helps Indonesian users inspect four SerpApi response types.
Run an offline replay first, then make one live request with your own credential.

```bash
export SERPAPI_API_KEY="your_key"
python3 serp_idi_tracker.py --keyword "coffee in Bogor"
python3 serp_idi_tracker.py --engine google_maps --keyword "kafe bogor" --offline
python3 -m unittest discover -s tests -v
```

Offline output uses the stored sample's original query. It is not a fresh search.
The CLI rejects API error payloads and unfinished searches, and distinguishes an
absent result field from an empty array. Authentication and quota failures return
an error without printing the raw response body or credential-bearing URL.

This is a response explorer, not a complete rank monitoring service. No adoption,
classification accuracy, customer growth or live reliability claim is made.
The original 2024 workflow mentioned in my application is not this repository.

## Verify and contribute

```bash
python3 -m unittest discover -s tests -v
```

Tests cover response fields, errors, localization parameters, offline replay and
documentation links. They run without API keys. GitHub Actions runs the same suite.

To report a problem, include the engine, command with credentials removed,
expected output and actual behavior. Use [the feedback template](docs/user-feedback-template.md)
to record a learner's setup friction. Do not include API keys or private user data.

[Contribution guide](CONTRIBUTING.md) · [Validation record](VERIFICATION.md)

## Sources and attribution

These are original educational explanations referencing the official
[Search](https://serpapi.com/search-api), [News](https://serpapi.com/google-news-api),
[Maps](https://serpapi.com/google-maps-api),
[Autocomplete](https://serpapi.com/google-autocomplete-api) and
[error code](https://serpapi.com/api-status-and-error-codes) documentation.
Reviewed on 15 October 2026. Sample provenance is described in
[samples/README.md](samples/README.md). Code is MIT licensed; SerpApi branding and
third-party search content remain subject to their respective rights.
