"""
Simple Personal Finance Tracker
Aplikasi pencatatan dan pengelolaan keuangan pribadi berbasis terminal (CLI).
Menggunakan pustaka standar Python (csv, os, datetime) tanpa dependensi eksternal.
"""

import csv
import os
from datetime import datetime

# ==============================================================================
# KONSTANTA KONFIGURASI (Menggunakan path relatif agar mudah dijalankan)
# ==============================================================================
NAMA_FILE_DATA = "transaksi.csv"
KOLOM_CSV = ["tanggal", "jenis", "kategori", "keterangan", "nominal"]


# ==============================================================================
# FUNGSI BANTU (UTILITY)
# ==============================================================================
def format_rupiah(angka):
    """Mengubah angka (int/float) menjadi format mata uang Rupiah, mis. Rp 25.000."""
    tanda = "-" if angka < 0 else ""
    nilai_absolut = abs(int(round(angka)))
    # Format dengan pemisah ribuan koma, lalu ganti koma menjadi titik (standar Indonesia)
    formatted = f"{nilai_absolut:,}".replace(",", ".")
    return f"{tanda}Rp {formatted}"


def cetak_garis(panjang=82, karakter="="):
    """Mencetak garis pemisah di terminal agar tampilan lebih rapi."""
    print(karakter * panjang)


# ==============================================================================
# FUNGSI PENYIMPANAN & PEMBACAAN CSV (PERSISTENCE)
# ==============================================================================
def muat_transaksi(nama_file=NAMA_FILE_DATA):
    """
    Membaca seluruh data transaksi dari file CSV.
    Menangani FileNotFoundError saat aplikasi pertama kali dijalankan
    (ketika file CSV belum ada) serta melewati baris yang rusak.
    """
    daftar_transaksi = []
    try:
        with open(nama_file, mode="r", encoding="utf-8", newline="") as file:
            pembaca = csv.DictReader(file)
            for nomor_baris, baris in enumerate(pembaca, start=2):
                try:
                    # Pastikan seluruh kolom wajib tersedia dan nominal berupa angka valid
                    tanggal = baris["tanggal"].strip()
                    jenis = baris["jenis"].strip().lower()
                    kategori = baris["kategori"].strip()
                    keterangan = baris["keterangan"].strip()
                    nominal = int(float(baris["nominal"].strip()))

                    # Validasi isi dasar agar data yang rusak tidak merusak perhitungan
                    datetime.strptime(tanggal, "%Y-%m-%d")
                    if jenis not in ("pemasukan", "pengeluaran") or nominal <= 0:
                        continue

                    daftar_transaksi.append({
                        "tanggal": tanggal,
                        "jenis": jenis,
                        "kategori": kategori,
                        "keterangan": keterangan,
                        "nominal": nominal,
                    })
                except (KeyError, ValueError, AttributeError):
                    # Baris rusak/tidak lengkap dilewati agar program tidak berhenti mendadak
                    print(f"[Peringatan] Baris ke-{nomor_baris} pada '{nama_file}' tidak valid dan dilewati.")
    except FileNotFoundError:
        # Kondisi normal pada pemakaian pertama kali: kembalikan list kosong
        return []
    except OSError as error:
        print(f"[Error] Gagal membaca file '{nama_file}': {error}")
        return []

    return daftar_transaksi


def simpan_transaksi(transaksi, nama_file=NAMA_FILE_DATA):
    """
    Menambahkan satu transaksi baru ke akhir file CSV menggunakan mode 'a' (append).
    Jika file belum ada atau masih kosong, header kolom ditulis terlebih dahulu.
    """
    file_baru = (not os.path.exists(nama_file)) or (os.path.getsize(nama_file) == 0)

    with open(nama_file, mode="a", encoding="utf-8", newline="") as file:
        penulis = csv.DictWriter(file, fieldnames=KOLOM_CSV)
        if file_baru:
            penulis.writeheader()
        penulis.writerow(transaksi)


# ==============================================================================
# FUNGSI VALIDASI INPUT PENGGUNA
# ==============================================================================
def input_tanggal():
    """
    Meminta input tanggal berformat YYYY-MM-DD.
    Jika pengguna langsung menekan Enter, otomatis menggunakan tanggal hari ini.
    """
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    while True:
        teks = input(f"Tanggal (YYYY-MM-DD) [Enter untuk {hari_ini}]: ").strip()
        if teks == "":
            return hari_ini
        try:
            # Validasi apakah tanggal benar-benar valid di kalender (mis. bukan 2026-02-30)
            datetime.strptime(teks, "%Y-%m-%d")
            return teks
        except ValueError:
            print("  [!] Format tanggal tidak valid. Gunakan format YYYY-MM-DD (contoh: 2026-11-15).")


def input_jenis():
    """Meminta pengguna memilih jenis transaksi: pemasukan atau pengeluaran."""
    while True:
        print("Pilih jenis transaksi:")
        print("  1. Pemasukan")
        print("  2. Pengeluaran")
        pilihan = input("Masukkan pilihan (1/2): ").strip().lower()
        if pilihan in ("1", "pemasukan"):
            return "pemasukan"
        if pilihan in ("2", "pengeluaran"):
            return "pengeluaran"
        print("  [!] Pilihan tidak valid. Ketik 1 untuk Pemasukan atau 2 untuk Pengeluaran.")


def input_teks_wajib(prompt):
    """Meminta input teks yang tidak boleh kosong."""
    while True:
        nilai = input(prompt).strip()
        if nilai != "":
            return nilai
        print("  [!] Input tidak boleh kosong. Silakan isi kembali.")


def input_nominal():
    """
    Meminta input nominal transaksi.
    Harus berupa angka bulat/desimal valid dan lebih besar dari nol (> 0).
    """
    while True:
        teks = input("Nominal (Rp, angka saja mis. 25000): ").strip()
        # Hapus titik atau koma pemisah ribuan jika pengguna tidak sengaja mengetiknya
        teks_bersih = teks.replace(".", "").replace(",", "")
        try:
            nominal = int(teks_bersih)
            if nominal <= 0:
                print("  [!] Nominal harus lebih besar dari 0.")
                continue
            return nominal
        except ValueError:
            print("  [!] Input tidak valid. Nominal harus berupa angka positif (contoh: 25000).")


def input_bulan():
    """Meminta input bulan laporan dalam format YYYY-MM (contoh: 2026-11)."""
    bulan_ini = datetime.now().strftime("%Y-%m")
    while True:
        teks = input(f"Masukkan bulan (YYYY-MM) [Enter untuk {bulan_ini}]: ").strip()
        if teks == "":
            return bulan_ini
        try:
            datetime.strptime(teks, "%Y-%m")
            return teks
        except ValueError:
            print("  [!] Format bulan tidak valid. Gunakan format YYYY-MM (contoh: 2026-11).")


# ==============================================================================
# FITUR 1: MANAJEMEN TRANSAKSI (TAMBAH DATA)
# ==============================================================================
def tambah_transaksi(daftar_transaksi, nama_file=NAMA_FILE_DATA):
    """Menambah transaksi baru, menyimpannya ke CSV, dan memperbarui list di memori."""
    print()
    cetak_garis()
    print("TAMBAH TRANSAKSI BARU")
    cetak_garis()

    tanggal = input_tanggal()
    jenis = input_jenis()
    kategori = input_teks_wajib("Kategori (mis. Makanan, Transport, Gaji, Uang Saku): ")
    keterangan = input_teks_wajib("Keterangan singkat: ")
    nominal = input_nominal()

    transaksi_baru = {
        "tanggal": tanggal,
        "jenis": jenis,
        "kategori": kategori,
        "keterangan": keterangan,
        "nominal": nominal,
    }

    simpan_transaksi(transaksi_baru, nama_file)
    daftar_transaksi.append(transaksi_baru)

    print(f"\n[Sukses] Transaksi {jenis} sebesar {format_rupiah(nominal)} berhasil disimpan.")


# ==============================================================================
# FITUR 2: MENAMPILKAN & MEMFILTER TRANSAKSI
# ==============================================================================
def tampilkan_tabel_transaksi(daftar_transaksi, judul="DAFTAR TRANSAKSI"):
    """Menampilkan daftar transaksi dalam bentuk tabel terminal yang rapi."""
    print()
    cetak_garis()
    print(judul)
    cetak_garis()

    if not daftar_transaksi:
        print("Belum ada data transaksi yang sesuai.")
        cetak_garis()
        return

    # Header tabel dengan lebar kolom tetap agar lurus
    print(f"{'No':<4} {'Tanggal':<12} {'Jenis':<13} {'Kategori':<15} {'Keterangan':<20} {'Nominal':>12}")
    cetak_garis(karakter="-")

    total = 0
    for indeks, trx in enumerate(daftar_transaksi, start=1):
        # Potong keterangan jika terlalu panjang agar tabel tidak berantakan
        ket_tampil = trx["keterangan"]
        if len(ket_tampil) > 19:
            ket_tampil = ket_tampil[:16] + "..."

        kat_tampil = trx["kategori"]
        if len(kat_tampil) > 14:
            kat_tampil = kat_tampil[:11] + "..."

        print(
            f"{indeks:<4} {trx['tanggal']:<12} {trx['jenis']:<13} "
            f"{kat_tampil:<15} {ket_tampil:<20} {format_rupiah(trx['nominal']):>12}"
        )
        total += trx["nominal"]

    cetak_garis(karakter="-")
    print(f"Total transaksi ditampilkan: {len(daftar_transaksi)} | Jumlah nominal: {format_rupiah(total)}")
    cetak_garis()


def filter_transaksi(daftar_transaksi, jenis_filter=None):
    """
    Mengembalikan list transaksi yang sudah difilter berdasarkan jenis.
    Jika jenis_filter=None, mengembalikan semua transaksi.
    """
    if jenis_filter is None:
        return list(daftar_transaksi)
    return [trx for trx in daftar_transaksi if trx["jenis"] == jenis_filter]


def menu_lihat_transaksi(daftar_transaksi):
    """Sub-menu untuk memilih tampilan semua transaksi, hanya pemasukan, atau hanya pengeluaran."""
    print()
    cetak_garis()
    print("LIHAT & FILTER TRANSAKSI")
    cetak_garis()
    print("1. Tampilkan Semua Transaksi")
    print("2. Filter: Hanya Pemasukan")
    print("3. Filter: Hanya Pengeluaran")
    print("0. Kembali ke Menu Utama")

    pilihan = input("Pilih tampilan (0-3): ").strip()
    if pilihan == "1":
        tampilkan_tabel_transaksi(filter_transaksi(daftar_transaksi), "SEMUA TRANSAKSI")
    elif pilihan == "2":
        data_masuk = filter_transaksi(daftar_transaksi, "pemasukan")
        tampilkan_tabel_transaksi(data_masuk, "TRANSAKSI PEMASUKAN")
    elif pilihan == "3":
        data_keluar = filter_transaksi(daftar_transaksi, "pengeluaran")
        tampilkan_tabel_transaksi(data_keluar, "TRANSAKSI PENGELUARAN")
    elif pilihan == "0":
        return
    else:
        print("  [!] Pilihan tidak valid.")


# ==============================================================================
# FITUR 3: LAPORAN KEUANGAN BULANAN
# ==============================================================================
def hitung_laporan_bulanan(daftar_transaksi, bulan):
    """
    Menghitung ringkasan keuangan khusus untuk satu bulan (format YYYY-MM).
    Mengembalikan dictionary berisi total pemasukan, pengeluaran, saldo,
    rincian pengeluaran per kategori, kategori terbesar, dan saving rate.
    """
    # Ambil hanya transaksi yang tanggalnya diawali 'YYYY-MM'
    transaksi_bulan = [trx for trx in daftar_transaksi if trx["tanggal"].startswith(bulan)]

    total_pemasukan = 0
    total_pengeluaran = 0
    pengeluaran_per_kategori = {}

    for trx in transaksi_bulan:
        if trx["jenis"] == "pemasukan":
            total_pemasukan += trx["nominal"]
        elif trx["jenis"] == "pengeluaran":
            total_pengeluaran += trx["nominal"]
            kat = trx["kategori"]
            # Akumulasi pengeluaran ke dalam dictionary per kategori
            pengeluaran_per_kategori[kat] = pengeluaran_per_kategori.get(kat, 0) + trx["nominal"]

    saldo = total_pemasukan - total_pengeluaran

    # Tentukan kategori pengeluaran terbesar (jika ada pengeluaran)
    if pengeluaran_per_kategori:
        kategori_terbesar = max(pengeluaran_per_kategori, key=pengeluaran_per_kategori.get)
        nominal_terbesar = pengeluaran_per_kategori[kategori_terbesar]
    else:
        kategori_terbesar = "-"
        nominal_terbesar = 0

    # Hitung saving rate dengan mencegah pembagian dengan nol (ZeroDivisionError)
    if total_pemasukan > 0:
        saving_rate = ((total_pemasukan - total_pengeluaran) / total_pemasukan) * 100
        saving_rate_teks = f"{saving_rate:.2f}%"
    else:
        saving_rate = None
        saving_rate_teks = "Tidak dapat dihitung (pemasukan Rp 0)"

    return {
        "bulan": bulan,
        "jumlah_transaksi": len(transaksi_bulan),
        "total_pemasukan": total_pemasukan,
        "total_pengeluaran": total_pengeluaran,
        "saldo": saldo,
        "pengeluaran_per_kategori": pengeluaran_per_kategori,
        "kategori_terbesar": kategori_terbesar,
        "nominal_terbesar": nominal_terbesar,
        "saving_rate": saving_rate,
        "saving_rate_teks": saving_rate_teks,
    }


def tampilkan_laporan_bulanan(daftar_transaksi):
    """Meminta bulan dari pengguna lalu mencetak laporan keuangan bulanan ke terminal."""
    print()
    cetak_garis()
    print("LAPORAN KEUANGAN BULANAN")
    cetak_garis()

    bulan = input_bulan()
    laporan = hitung_laporan_bulanan(daftar_transaksi, bulan)

    print()
    cetak_garis()
    print(f"RINGKASAN KEUANGAN BULAN {laporan['bulan']}")
    cetak_garis()

    if laporan["jumlah_transaksi"] == 0:
        print(f"Tidak ditemukan transaksi pada bulan {bulan}.")
        cetak_garis()
        return

    print(f"Jumlah Transaksi             : {laporan['jumlah_transaksi']}")
    print(f"Total Pemasukan              : {format_rupiah(laporan['total_pemasukan'])}")
    print(f"Total Pengeluaran            : {format_rupiah(laporan['total_pengeluaran'])}")
    print(f"Saldo Bulanan                : {format_rupiah(laporan['saldo'])}")
    print(f"Persentase Tabungan (Saving) : {laporan['saving_rate_teks']}")

    if laporan["kategori_terbesar"] != "-":
        print(
            f"Kategori Pengeluaran Terbesar: {laporan['kategori_terbesar']} "
            f"({format_rupiah(laporan['nominal_terbesar'])})"
        )
    else:
        print("Kategori Pengeluaran Terbesar: Belum ada pengeluaran")

    print("\nRincian Pengeluaran per Kategori:")
    cetak_garis(panjang=52, karakter="-")
    if laporan["pengeluaran_per_kategori"]:
        # Urutkan kategori dari pengeluaran terbesar ke terkecil
        urutan = sorted(
            laporan["pengeluaran_per_kategori"].items(),
            key=lambda item: item[1],
            reverse=True,
        )
        for kat, jumlah in urutan:
            persen = (jumlah / laporan["total_pengeluaran"]) * 100
            print(f"  {kat:<22} : {format_rupiah(jumlah):>14} ({persen:5.1f}%)")
    else:
        print("  (Tidak ada pengeluaran pada bulan ini)")
    cetak_garis()


# ==============================================================================
# FITUR 4: EKSPOR DATA TRANSAKSI & RINGKASAN BULANAN KE CSV
# ==============================================================================
def ekspor_data_transaksi(daftar_transaksi, nama_file="ekspor_transaksi.csv"):
    """Mengekspor seluruh data transaksi ke file CSV baru menggunakan mode 'w'."""
    with open(nama_file, mode="w", encoding="utf-8", newline="") as file:
        penulis = csv.DictWriter(file, fieldnames=KOLOM_CSV)
        penulis.writeheader()
        penulis.writerows(daftar_transaksi)
    print(f"[Sukses] {len(daftar_transaksi)} transaksi berhasil diekspor ke '{nama_file}'.")


def ekspor_ringkasan_bulanan(daftar_transaksi, bulan, nama_file=None):
    """Mengekspor hasil laporan keuangan bulanan ke file CSV terstruktur."""
    laporan = hitung_laporan_bulanan(daftar_transaksi, bulan)
    if nama_file is None:
        nama_file = f"ringkasan_bulanan_{bulan}.csv"

    with open(nama_file, mode="w", encoding="utf-8", newline="") as file:
        penulis = csv.writer(file)
        # Bagian 1: Ringkasan Umum
        penulis.writerow(["Ringkasan Keuangan Bulanan", bulan])
        penulis.writerow(["Metrik", "Nilai"])
        penulis.writerow(["Jumlah Transaksi", laporan["jumlah_transaksi"]])
        penulis.writerow(["Total Pemasukan", laporan["total_pemasukan"]])
        penulis.writerow(["Total Pengeluaran", laporan["total_pengeluaran"]])
        penulis.writerow(["Saldo Bulanan", laporan["saldo"]])
        penulis.writerow(["Kategori Pengeluaran Terbesar", laporan["kategori_terbesar"]])
        penulis.writerow(["Nominal Kategori Terbesar", laporan["nominal_terbesar"]])
        penulis.writerow(["Saving Rate", laporan["saving_rate_teks"]])
        penulis.writerow([])

        # Bagian 2: Rincian Pengeluaran per Kategori
        penulis.writerow(["Rincian Pengeluaran per Kategori", "Nominal", "Persentase"])
        if laporan["pengeluaran_per_kategori"]:
            urutan = sorted(
                laporan["pengeluaran_per_kategori"].items(),
                key=lambda item: item[1],
                reverse=True,
            )
            for kat, jumlah in urutan:
                persen = (jumlah / laporan["total_pengeluaran"]) * 100
                penulis.writerow([kat, jumlah, f"{persen:.1f}%"])
        else:
            penulis.writerow(["Tidak ada pengeluaran", 0, "0.0%"])

    print(f"[Sukses] Ringkasan bulan {bulan} berhasil diekspor ke '{nama_file}'.")


def menu_ekspor_csv(daftar_transaksi):
    """Sub-menu untuk mengekspor data transaksi atau ringkasan bulanan ke CSV."""
    print()
    cetak_garis()
    print("EKSPOR DATA KE CSV")
    cetak_garis()
    print("1. Ekspor Semua Data Transaksi (ekspor_transaksi.csv)")
    print("2. Ekspor Ringkasan Keuangan Bulanan (ringkasan_bulanan_YYYY-MM.csv)")
    print("0. Kembali ke Menu Utama")

    pilihan = input("Pilih jenis ekspor (0-2): ").strip()
    if pilihan == "1":
        if not daftar_transaksi:
            print("  [!] Belum ada data transaksi untuk diekspor.")
            return
        ekspor_data_transaksi(daftar_transaksi)
    elif pilihan == "2":
        bulan = input_bulan()
        ekspor_ringkasan_bulanan(daftar_transaksi, bulan)
    elif pilihan == "0":
        return
    else:
        print("  [!] Pilihan tidak valid.")


# ==============================================================================
# FITUR 5: DASHBOARD SEDERHANA (RINGKASAN SALDO & TRANSAKSI TERBARU)
# ==============================================================================
def tampilkan_dashboard(daftar_transaksi):
    """Menampilkan ringkasan saldo total dan maksimal 5 transaksi terbaru di menu utama."""
    total_masuk = sum(trx["nominal"] for trx in daftar_transaksi if trx["jenis"] == "pemasukan")
    total_keluar = sum(trx["nominal"] for trx in daftar_transaksi if trx["jenis"] == "pengeluaran")
    saldo = total_masuk - total_keluar

    print()
    cetak_garis()
    print("SIMPLE PERSONAL FINANCE TRACKER - DASHBOARD")
    cetak_garis()
    print(f"Total Pemasukan   : {format_rupiah(total_masuk)}")
    print(f"Total Pengeluaran : {format_rupiah(total_keluar)}")
    print(f"Saldo Saat Ini    : {format_rupiah(saldo)}")
    print(f"Jumlah Transaksi  : {len(daftar_transaksi)}")
    cetak_garis(karakter="-")
    print("5 Transaksi Terbaru:")

    if not daftar_transaksi:
        print("  (Belum ada transaksi. Pilih menu 1 untuk mulai mencatat.)")
    else:
        # Ambil 5 transaksi paling akhir lalu balik urutannya agar yang terbaru di atas
        terbaru = daftar_transaksi[-5:][::-1]
        for trx in terbaru:
            tanda = "+" if trx["jenis"] == "pemasukan" else "-"
            print(
                f"  [{trx['tanggal']}] {tanda} {format_rupiah(trx['nominal']):<13} "
                f"| {trx['kategori']:<13} | {trx['keterangan']}"
            )
    cetak_garis()


# ==============================================================================
# PROGRAM UTAMA (MAIN LOOP)
# ==============================================================================
def main():
    """Titik masuk utama aplikasi: memuat data CSV lalu menjalankan menu berulang."""
    daftar_transaksi = muat_transaksi(NAMA_FILE_DATA)

    try:
        while True:
            tampilkan_dashboard(daftar_transaksi)
            print("MENU UTAMA:")
            print("  1. Tambah Transaksi (Pemasukan / Pengeluaran)")
            print("  2. Lihat & Filter Transaksi")
            print("  3. Laporan Keuangan Bulanan")
            print("  4. Ekspor Data ke CSV")
            print("  5. Keluar")

            pilihan = input("\nPilih menu (1-5): ").strip()

            if pilihan == "1":
                tambah_transaksi(daftar_transaksi, NAMA_FILE_DATA)
            elif pilihan == "2":
                menu_lihat_transaksi(daftar_transaksi)
            elif pilihan == "3":
                tampilkan_laporan_bulanan(daftar_transaksi)
            elif pilihan == "4":
                menu_ekspor_csv(daftar_transaksi)
            elif pilihan == "5":
                print("\nTerima kasih telah menggunakan Simple Personal Finance Tracker. Sampai jumpa!")
                break
            else:
                print("\n  [!] Pilihan menu tidak valid. Silakan pilih angka 1 sampai 5.")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C). Data yang sudah tersimpan tetap aman.")


if __name__ == "__main__":
    main()
