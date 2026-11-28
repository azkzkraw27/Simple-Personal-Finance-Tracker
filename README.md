# Simple Personal Finance Tracker (Python CLI)

Aplikasi pencatat keuangan pribadi berbasis terminal (*Command Line Interface*) yang dibuat menggunakan **Python 3 standar** (tanpa perlu menginstal library tambahan seperti `pandas` atau `numpy`). Dirancang dengan struktur kode yang ramah dipahami mahasiswa semester 1 serta arsitektur fungsi mandiri (*decoupled*) sehingga aman apabila salah satu fungsi dihapus atau dimodifikasi.

---

## Daftar Isi
1. [Fitur Utama](#1-fitur-utama)
2. [Persiapan & Persyaratan Sistem](#2-persiapan--persyaratan-sistem)
3. [Struktur Folder Proyek](#3-struktur-folder-proyek)
4. [Tutorial Lengkap Menjalankan Program](#4-tutorial-lengkap-menjalankan-program)
5. [Tutorial Penggunaan Setiap Menu (Step-by-Step)](#5-tutorial-penggunaan-setiap-menu-step-by-step)
6. [Penjelasan Arsitektur Mandiri (Aman Saat Fungsi Dihapus)](#6-penjelasan-arsitektur-mandiri-aman-saat-fungsi-dihapus)
7. [Format File CSV](#7-format-file-csv)
8. [Troubleshooting (Solusi Masalah Umum)](#8-troubleshooting-solusi-masalah-umum)

---

## 1. Fitur Utama
- **Dashboard Ringkas Otomatis:** Langsung menampilkan total pemasukan, total pengeluaran, saldo akhir, jumlah transaksi, dan 5 transaksi terbaru setiap kali kembali ke menu utama.
- **Tambah Transaksi Tervalidasi:** Mencatat pemasukan atau pengeluaran dengan pemeriksaan otomatis pada format tanggal (`YYYY-MM-DD`), jenis transaksi, teks wajib, dan nominal angka positif (`> 0`).
- **Lihat & Filter Transaksi:** Menampilkan seluruh transaksi, khusus pemasukan, atau khusus pengeluaran dalam tabel terminal yang sejajar.
- **Laporan Keuangan Bulanan:** Menghitung ringkasan per bulan (`YYYY-MM`), total pemasukan/pengeluaran, saldo bulanan, pengeluaran terbesar, rincian per kategori, dan persentase tabungan (*saving rate*).
- **Penyimpanan Otomatis & Ekspor CSV:** Data tersimpan permanen di `transaksi.csv` dan dapat diekspor ke `ekspor_transaksi.csv` maupun `ringkasan_bulanan_YYYY-MM.csv` untuk dibuka di Microsoft Excel / Google Sheets.

---

## 2. Persiapan & Persyaratan Sistem
- **Python 3.8 atau lebih baru** (Sudah termasuk modul bawaan `csv`, `os`, dan `datetime`).
- **Terminal / Command Prompt / VS Code Terminal**.
- Tidak memerlukan koneksi internet maupun perintah `pip install`.

Cek apakah Python sudah terpasang di komputer kamu dengan mengetik di terminal:
```bash
python --version
# atau di macOS / Linux:
python3 --version
```

---

## 3. Struktur Folder Proyek
Pastikan seluruh file berada di dalam satu folder yang sama:
```text
Simple_Personal_Finance_Tracker/
├── finance_tracker.py              # Kode program utama Python
├── transaksi.csv                   # Database transaksi utama (otomatis dibuat/diperbarui)
├── ekspor_transaksi.csv            # Contoh hasil ekspor seluruh transaksi
├── ringkasan_bulanan_2026-11.csv   # Contoh hasil ekspor laporan bulanan
├── Laporan_Proyek_Akhir.pdf        # Laporan proyek lengkap beserta bedah setiap fungsi
└── README.md                       # Panduan dan tutorial penggunaan ini
```

---

## 4. Tutorial Lengkap Menjalankan Program

### Langkah 1: Ekstrak File ZIP
1. Klik kanan pada file `Simple_Personal_Finance_Tracker.zip`.
2. Pilih **Extract All...** (Windows) atau klik ganda (macOS).
3. Pastikan hasil ekstraksi membuka folder `Simple_Personal_Finance_Tracker`.

### Langkah 2: Buka Terminal di Folder Proyek
- **Cara Cepat (Windows):** Buka folder `Simple_Personal_Finance_Tracker` di File Explorer, klik bilah alamat (address bar) di bagian atas, ketik `cmd`, lalu tekan **Enter**.
- **Cara Cepat (VS Code):** Buka folder proyek di VS Code, lalu tekan `` Ctrl + ` `` (atau menu *Terminal -> New Terminal*).
- **Cara Manual via Terminal:**
  ```bash
  cd path/menuju/Simple_Personal_Finance_Tracker
  ```

### Langkah 3: Jalankan Aplikasi
Ketik salah satu perintah berikut di terminal:
```bash
python finance_tracker.py
```
Jika di macOS/Linux perintah `python` tidak dikenali, gunakan:
```bash
python3 finance_tracker.py
```

---

## 5. Tutorial Penggunaan Setiap Menu (Step-by-Step)

Begitu program berjalan, layar akan menampilkan **Dashboard** dan **5 pilihan Menu Utama**:

### Menu 1: Tambah Transaksi
1. Ketik `1` lalu tekan **Enter**.
2. **Tanggal:** Ketik tanggal dengan format `YYYY-MM-DD` (contoh: `2026-11-28`), atau langsung tekan **Enter** untuk memakai tanggal hari ini secara otomatis.
3. **Jenis Transaksi:** Ketik `1` untuk *Pemasukan* atau `2` untuk *Pengeluaran*.
4. **Kategori:** Ketik nama kategori, misalnya `Makanan`, `Kost`, `Transportasi`, atau `Uang Saku` (tidak boleh kosong).
5. **Keterangan:** Ketik catatan singkat, misalnya `Makan siang di kantin`.
6. **Nominal:** Ketik angka saja tanpa `Rp`, misalnya `25000` (jika tidak sengaja mengetik `25.000`, program tetap membersihkannya otomatis).
7. Data langsung tersimpan ke `transaksi.csv` dan saldo dashboard diperbarui.

### Menu 2: Lihat & Filter Transaksi
1. Ketik `2` lalu tekan **Enter**.
2. Pilih tampilan yang diinginkan:
   - `1` → Menampilkan **semua** transaksi.
   - `2` → Menampilkan **hanya pemasukan**.
   - `3` → Menampilkan **hanya pengeluaran**.
   - `0` → Kembali ke menu utama.

### Menu 3: Laporan Keuangan Bulanan
1. Ketik `3` lalu tekan **Enter**.
2. Masukkan bulan dengan format `YYYY-MM` (contoh: `2026-11`), atau tekan **Enter** untuk melihat bulan berjalan.
3. Program akan menampilkan:
   - Total pemasukan, total pengeluaran, dan saldo bulan tersebut.
   - **Saving Rate** (persentase sisa pemasukan yang berhasil ditabung).
   - **Kategori Pengeluaran Terbesar** beserta rincian persentase setiap kategori.

### Menu 4: Ekspor Data ke CSV
1. Ketik `4` lalu tekan **Enter**.
2. Pilih jenis file CSV yang ingin dibuat:
   - `1` → Membuat file `ekspor_transaksi.csv` berisi seluruh catatan transaksi.
   - `2` → Membuat file `ringkasan_bulanan_YYYY-MM.csv` berisi rekap laporan bulanan yang siap dibuka di Microsoft Excel.

### Menu 5: Keluar
- Ketik `5` lalu tekan **Enter** untuk menutup program dengan aman. (Jika menekan `Ctrl + C`, program juga akan berhenti rapi tanpa merusak file CSV).

---

## 6. Penjelasan Arsitektur Mandiri (Aman Saat Fungsi Dihapus)

Kode `finance_tracker.py` dirancang menggunakan prinsip **Loose Coupling (Keterikatan Longgar)** agar cocok dipelajari mahasiswa semester 1 maupun saat pembagian tugas kelompok:

1. **Setiap Fungsi Utama Bekerja Mandiri:**
   Fungsi fitur utama (`tambah_transaksi`, `menu_lihat_transaksi`, `tampilkan_laporan_bulanan`, `menu_ekspor_csv`, dan `tampilkan_dashboard`) tidak saling memaksa memanggil fungsi bantu eksternal di dalam tubuh utamanya. Misalnya, jika kamu menghapus `format_rupiah()`, `cetak_garis()`, `input_tanggal()`, atau `filter_transaksi()`, fitur-fitur utama lainnya **tetap berjalan normal tanpa `NameError`**.
2. **Pemanggilan Aman di `main()` melalui `panggil_aman()`:**
   Menu utama menggunakan helper `panggil_aman("nama_fungsi", ...)` yang mengecek `globals().get(nama_fungsi)` terlebih dahulu. Jika salah satu fungsi fitur dihapus atau dikomentari (`#`), program tidak akan crash—melainkan menampilkan pesan informasi bahwa fitur tersebut sedang dinonaktifkan.

---

## 7. Format File CSV
File `transaksi.csv` menggunakan pemisah koma (`,`) dengan 5 kolom standar:

| Kolom | Format | Contoh | Keterangan |
| :--- | :--- | :--- | :--- |
| `tanggal` | `YYYY-MM-DD` | `2026-11-12` | Tahun-Bulan-Tanggal |
| `jenis` | teks kecil | `pengeluaran` | Hanya `pemasukan` atau `pengeluaran` |
| `kategori` | teks bebas | `Makanan` | Kelompok pos anggaran |
| `keterangan` | teks bebas | `Makan siang kantin` | Penjelasan singkat transaksi |
| `nominal` | bilangan bulat | `55000` | Nominal dalam Rupiah tanpa simbol |

---

## 8. Troubleshooting (Solusi Masalah Umum)
- **`python: command not found`:** Coba jalankan menggunakan `python3 finance_tracker.py` atau `py finance_tracker.py` (Windows).
- **`No such file or directory: 'finance_tracker.py'`:** Pastikan terminal kamu sudah berada di dalam folder `Simple_Personal_Finance_Tracker` (cek dengan perintah `dir` di Windows atau `ls` di macOS/Linux).
- **File CSV berantakan saat dibuka di Excel:** Di Excel, gunakan menu **Data -> From Text/CSV**, lalu pilih delimiter **Comma (Koma)** dan encoding **UTF-8**.
