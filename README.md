# Simple Personal Finance Tracker

Aplikasi pencatatan dan pengelolaan keuangan pribadi berbasis terminal (CLI) yang dibuat menggunakan Python standar tanpa pustaka eksternal.

## Fitur Utama
1. **Dashboard Sederhana**: Menampilkan ringkasan total pemasukan, total pengeluaran, saldo saat ini, jumlah transaksi, serta 5 transaksi terbaru pada menu utama.
2. **Manajemen Transaksi**: Menambah transaksi pemasukan atau pengeluaran lengkap dengan tanggal (`YYYY-MM-DD`), kategori, keterangan singkat, dan nominal tervalidasi.
3. **Menampilkan & Memfilter Transaksi**: Menampilkan seluruh transaksi, hanya pemasukan, atau hanya pengeluaran dalam tabel terminal.
4. **Laporan Keuangan Bulanan**: Menghitung total pemasukan, total pengeluaran, saldo bulanan, rincian pengeluaran per kategori, kategori pengeluaran terbesar, dan persentase tabungan (*saving rate*) untuk bulan tertentu (`YYYY-MM`).
5. **Penyimpanan & Ekspor CSV**: Menyimpan transaksi secara otomatis ke `transaksi.csv` (tetap terbaca saat aplikasi dibuka ulang) serta mengekspor data transaksi (`ekspor_transaksi.csv`) dan ringkasan bulanan (`ringkasan_bulanan_YYYY-MM.csv`).

## Persyaratan Sistem
- Python 3.8 atau lebih baru (tidak memerlukan instalasi paket tambahan).

## Cara Menjalankan Program
1. Ekstrak seluruh isi file ZIP ke dalam satu folder proyek.
2. Buka terminal / Command Prompt, lalu masuk ke folder proyek tersebut:
   ```bash
   cd Simple_Personal_Finance_Tracker
   ```
3. Jalankan program utama:
   ```bash
   python3 finance_tracker.py
   ```
   *(Di Windows, gunakan `python finance_tracker.py` jika perintah `python3` tidak tersedia.)*

## Daftar Berkas dalam Proyek
- `finance_tracker.py` — Source code utama aplikasi.
- `transaksi.csv` — Contoh data transaksi yang dihasilkan aplikasi.
- `ekspor_transaksi.csv` — Contoh file CSV hasil ekspor seluruh data transaksi.
- `ringkasan_bulanan_2026-11.csv` — Contoh file CSV hasil ekspor laporan bulanan November 2026.
- `Laporan_Proyek_Akhir.pdf` — Laporan kelompok proyek akhir.
- `README.md` — Petunjuk penggunaan program ini.
