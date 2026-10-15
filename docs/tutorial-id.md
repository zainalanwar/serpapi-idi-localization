# Membaca data tempat dari SerpApi

Tujuan latihan: pengguna Indonesia dapat menjalankan contoh, menemukan nama usaha
dan jumlah ulasannya, lalu membedakan data yang tersedia dari kesimpulan yang
masih memerlukan riset. Waktu latihan adalah rencana, bukan hasil uji pengguna.

## Mulai dengan masalah

Bayangkan Anda ingin memilih beberapa kafe Bogor untuk riset kompetitor. Anda
memerlukan daftar usaha dan atribut dasarnya sebelum membaca ulasan satu per satu.
API memberi data terstruktur; keputusan bisnis tetap membutuhkan konteks.

## Jalankan contoh

Dari root repo, jalankan:

```bash
python3 serp_idi_tracker.py --engine google_maps --keyword "kafe bogor" --offline
```

Cari satu nama usaha dalam output, lalu temukan item yang sama di
`samples/sample_google_maps.json`. Cocokkan `title`, `rating`, `reviews`, dan
`address` dalam `local_results`.

## Ubah menjadi request live

Isi `SERPAPI_API_KEY` di environment lokal dan jalankan perintah yang sama tanpa
`--offline`. Request dapat memakai kuota. Contoh mengirim `type=search`, `hl=id`
dan query dengan nama kota. Lihat dokumentasi Maps untuk parameter lokasi `ll`.

## Uji pemahaman

1. Mengapa `reviews` tidak memberi tahu alasan pelanggan kecewa?
2. Mengapa offline dengan keyword lain tetap menampilkan sample yang sama?
3. Apa perbedaan field hilang, array kosong, dan payload error?
4. Data apa lagi yang diperlukan sebelum menyarankan perubahan operasional?

## Bawa feedback ke perbaikan produk

Minta peserta menjelaskan langkah yang membingungkan. Catat gejala, instruksi
yang diikuti, dan hasil yang diharapkan. Reproduksi masalah dengan data yang telah
dihapus credential-nya, lalu tentukan apakah perbaikannya di tutorial, kode contoh,
atau perlu disampaikan kepada tim produk. Gunakan template feedback; jangan
mengisi hasil peserta sebelum sesi benar-benar dilakukan.
