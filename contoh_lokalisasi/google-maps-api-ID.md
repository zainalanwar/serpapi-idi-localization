# Membaca respons google_maps

Panduan edukasi Indonesia yang merujuk [dokumentasi resmi](https://serpapi.com/google-maps-api).
Ditinjau 15 Oktober 2026. Nama parameter dan field JSON dipertahankan agar
penjelasan dapat dicocokkan langsung dengan respons.

## Coba sample

```bash
python3 serp_idi_tracker.py --engine google_maps --keyword "kafe bogor" --offline
```

Perintah dijalankan dari root repo. Ini memutar satu sample tersimpan dan
menampilkan query aslinya; keyword baru hanya dipakai dalam mode live.

## Request live

Set `SERPAPI_API_KEY` secara lokal, lalu hilangkan `--offline`.
Tool mengirim `engine`, `q`, `api_key`, `hl=id` dan `type=search`.
Satu eksekusi default membuat satu request. Jangan mengirim key ke repo atau issue.

`hl` memilih bahasa pencarian. Pengaturan bahasa bukan jaminan semua hasil
berbahasa Indonesia. Nama kota dalam query membantu menentukan area; pelajari `ll` untuk kontrol lokasi Maps.

## Membaca hasil

Field utama: `local_results[]`. Field yang dibaca: `title`, `rating`, `reviews`, `address`.

Daftar tempat memakai `local_results`. `reviews` adalah jumlah ulasan, bukan teks ulasan. Data ini membantu memilih usaha yang akan diteliti; untuk membaca isi ulasan gunakan API yang sesuai. Respons pencarian berbeda dari detail satu tempat.

## Saat hasil tidak sesuai harapan

- HTTP 401: periksa credential tanpa membagikannya.
- HTTP 429: periksa kuota dan throughput sebelum mengulang.
- Payload `error`: request gagal; jangan menyebutnya hasil kosong.
- Status `Processing` atau `Queued`: tunggu respons selesai sebelum membaca hasil.
- Array kosong: respons memuat nol item pada bagian itu.
- Field tidak ada: periksa respons lengkap; bagian SERP tersebut mungkin tidak muncul.

## Latihan

Jelaskan satu item sample dengan kata-kata sendiri. Sebutkan satu keputusan yang
bisa dibantu data itu dan satu kesimpulan yang belum dapat dibuat.
Bandingkan field di sample dengan [sumber resmi](https://serpapi.com/google-maps-api) sebelum mengubah tutorial.
