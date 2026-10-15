# Membaca respons google_autocomplete

Panduan edukasi Indonesia yang merujuk [dokumentasi resmi](https://serpapi.com/google-autocomplete-api).
Ditinjau 15 Oktober 2026. Nama parameter dan field JSON dipertahankan agar
penjelasan dapat dicocokkan langsung dengan respons.

## Coba sample

```bash
python3 serp_idi_tracker.py --engine google_autocomplete --keyword "cara membuat" --offline
```

Perintah dijalankan dari root repo. Ini memutar satu sample tersimpan dan
menampilkan query aslinya; keyword baru hanya dipakai dalam mode live.

## Request live

Set `SERPAPI_API_KEY` secara lokal, lalu hilangkan `--offline`.
Tool mengirim `engine`, `q`, `api_key`, `gl=id` dan `hl=id`.
Satu eksekusi default membuat satu request. Jangan mengirim key ke repo atau issue.

`hl` memilih bahasa pencarian. Pengaturan bahasa bukan jaminan semua hasil
berbahasa Indonesia. `gl` memilih negara pencarian. Periksa dokumentasi engine sebelum menambah filter.

## Membaca hasil

Field utama: `suggestions[]`. Field yang dibaca: `value`; beberapa respons juga memuat `relevance` dan `type`.

Setiap saran dibaca dari `suggestions[].value`. Saran bukan angka search volume, niat pengguna yang terverifikasi, atau jaminan permintaan pasar. Gunakan sebagai ide yang masih perlu diuji.

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
Bandingkan field di sample dengan [sumber resmi](https://serpapi.com/google-autocomplete-api) sebelum mengubah tutorial.
