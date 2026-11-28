import csv
import os
from datetime import datetime


nama_file_data = "transaksi.csv"
kolom_csv = ["tanggal", "jenis", "kategori", "keterangan", "nominal"]

#INI ADALAH MEMANGGIL FUNGSI HANYA JIKA MASIH ADA PROGRAM NYA.
def panggil_aman(nama_fungsi, *data_argumen):
    
    fungsi = globals().get(nama_fungsi)
    if callable(fungsi):
        return fungsi(*data_argumen)
    print(f"\n[Info] Fungsi '{nama_fungsi}' sedang tidak tersedia/dihapus.")
    return None

# INI ADALAH FUNGSI MENGATUR NOMINAL UANG
def format_rupiah(angka):
    tanda = "-" if angka < 0 else ""
    nilai_bulat = abs(int(round(angka)))
    teks_angka = f"{nilai_bulat:,}".replace(",", ".")
    return f"{tanda}Rp {teks_angka}"

# INI ADALAH FUNGSI UNTUK MENGATUR GARIS PEMISAH DI TAMPILAN
def cetak_garis(panjang=80, karakter="="):
    print(karakter * panjang)

# INI ADALAH FUNGSI BACA & SIMPAN FILE CSV 
def muat_transaksi(nama_file=nama_file_data):
    daftar_transaksi = []

    if not os.path.exists(nama_file):
        return daftar_transaksi

    try:
        with open(nama_file, mode="r", encoding="utf-8", newline="") as file:
            pembaca = csv.DictReader(file)
            for nomor_baris, baris in enumerate(pembaca, start=2):
                try:
                    tanggal = baris["tanggal"].strip()
                    jenis = baris["jenis"].strip().lower()
                    kategori = baris["kategori"].strip()
                    keterangan = baris["keterangan"].strip()
                    nominal = int(float(baris["nominal"].strip()))

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
                    print(f"[Peringatan] Baris ke-{nomor_baris} rusak dan dilewati.")
    except OSError as error:
        print(f"[Error] Gagal membaca file '{nama_file}': {error}")

    return daftar_transaksi

def simpan_transaksi(transaksi_baru, nama_file=nama_file_data):
    file_baru = (not os.path.exists(nama_file)) or (os.path.getsize(nama_file) == 0)

    with open(nama_file, mode="a", encoding="utf-8", newline="") as file:
        penulis = csv.DictWriter(file, fieldnames=kolom_csv)
        if file_baru:
            penulis.writeheader()
        penulis.writerow(transaksi_baru)


# INI ADALAH FUNGSI VALIDASI INPUT PENGGUNA
def input_tanggal():
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    while True:
        teks = input(f"Tanggal (YYYY-MM-DD) [Enter untuk {hari_ini}]: ").strip()
        if teks == "":
            return hari_ini
        try:
            datetime.strptime(teks, "%Y-%m-%d")
            return teks
        except ValueError:
            print("  [!] Format tanggal salah. Gunakan YYYY-MM-DD (contoh: 2026-11-15).")

def input_jenis():
    while True:
        print("Pilih jenis transaksi:")
        print("  1. Pemasukan")
        print("  2. Pengeluaran")
        pilihan = input("Masukkan pilihan (1/2): ").strip().lower()
        if pilihan in ("1", "pemasukan"):
            return "pemasukan"
        elif pilihan in ("2", "pengeluaran"):
            return "pengeluaran"
        else:
            print("  [!] Pilihan tidak valid. Ketik 1 atau 2.")

def input_teks_wajib(pesan):
    while True:
        nilai = input(pesan).strip()
        if nilai != "":
            return nilai
        print("  [!] Input tidak boleh kosong. Silakan isi lagi.")

def input_nominal():
    while True:
        teks = input("Nominal (Rp, angka saja mis. 25000): ").strip()
        teks_bersih = teks.replace(".", "").replace(",", "")
        try:
            nominal = int(teks_bersih)
            if nominal > 0:
                return nominal
            print("  [!] Nominal harus lebih besar dari 0.")
        except ValueError:
            print("  [!] Input tidak valid. Masukkan angka positif (contoh: 25000).")


def input_bulan():
    bulan_ini = datetime.now().strftime("%Y-%m")
    while True:
        teks = input(f"Masukkan bulan (YYYY-MM) [Enter untuk {bulan_ini}]: ").strip()
        if teks == "":
            return bulan_ini
        try:
            datetime.strptime(teks, "%Y-%m")
            return teks
        except ValueError:
            print("  [!] Format bulan salah. Gunakan YYYY-MM (contoh: 2026-11).")


# FITUR 1: TAMBAH TRANSAKSI
def tambah_transaksi(daftar_transaksi, nama_file=nama_file_data):
    print()
    cetak_garis()
    print("TAMBAH TRANSAKSI BARU")
    cetak_garis()

    tanggal = input_tanggal()
    jenis = input_jenis()
    kategori = input_teks_wajib("Kategori (mis. Makanan, Kost, Transport, Uang Saku): ")
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


# FITUR 2: LIHAT & FILTER TRANSAKSI
def tampilkan_tabel_transaksi(daftar_tampil, judul="DAFTAR TRANSAKSI"):
    """Mencetak daftar transaksi dalam bentuk tabel terminal."""
    print()
    cetak_garis()
    print(judul)
    cetak_garis()

    if len(daftar_tampil) == 0:
        print("Belum ada data transaksi yang sesuai.")
        cetak_garis()
        return

    print(f"{'No':<4} {'Tanggal':<12} {'Jenis':<13} {'Kategori':<15} {'Keterangan':<20} {'Nominal':>12}")
    cetak_garis(karakter="-")

    total_nominal = 0
    for nomor, transaksi in enumerate(daftar_tampil, start=1):
        keterangan_tampil = transaksi["keterangan"]
        if len(keterangan_tampil) > 19:
            keterangan_tampil = keterangan_tampil[:16] + "..."

        kategori_tampil = transaksi["kategori"]
        if len(kategori_tampil) > 14:
            kategori_tampil = kategori_tampil[:11] + "..."

        print(
            f"{nomor:<4} {transaksi['tanggal']:<12} {transaksi['jenis']:<13} "
            f"{kategori_tampil:<15} {keterangan_tampil:<20} {format_rupiah(transaksi['nominal']):>12}"
        )
        total_nominal += transaksi["nominal"]

    cetak_garis(karakter="-")
    print(f"Total transaksi ditampilkan: {len(daftar_tampil)} | Jumlah nominal: {format_rupiah(total_nominal)}")
    cetak_garis()


def menu_lihat_transaksi(daftar_transaksi):
    """Sub-menu untuk melihat semua transaksi atau memfilter jenisnya."""
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
        tampilkan_tabel_transaksi(daftar_transaksi, "SEMUA TRANSAKSI")
    elif pilihan == "2":
        daftar_pemasukan = []
        for transaksi in daftar_transaksi:
            if transaksi["jenis"] == "pemasukan":
                daftar_pemasukan.append(transaksi)
        tampilkan_tabel_transaksi(daftar_pemasukan, "TRANSAKSI PEMASUKAN")
    elif pilihan == "3":
        daftar_pengeluaran = []
        for transaksi in daftar_transaksi:
            if transaksi["jenis"] == "pengeluaran":
                daftar_pengeluaran.append(transaksi)
        tampilkan_tabel_transaksi(daftar_pengeluaran, "TRANSAKSI PENGELUARAN")
    elif pilihan == "0":
        return
    else:
        print("  [!] Pilihan tidak valid.")


# FITUR 3: LAPORAN KEUANGAN BULANAN
def hitung_laporan_bulanan(daftar_transaksi, bulan):
    """Menghitung total pemasukan, pengeluaran, saldo, kategori, dan saving rate."""
    transaksi_bulan = []
    for transaksi in daftar_transaksi:
        if transaksi["tanggal"].startswith(bulan):
            transaksi_bulan.append(transaksi)

    total_pemasukan = 0
    total_pengeluaran = 0
    pengeluaran_kategori = {}

    for transaksi in transaksi_bulan:
        if transaksi["jenis"] == "pemasukan":
            total_pemasukan += transaksi["nominal"]
        elif transaksi["jenis"] == "pengeluaran":
            total_pengeluaran += transaksi["nominal"]
            nama_kategori = transaksi["kategori"]
            if nama_kategori not in pengeluaran_kategori:
                pengeluaran_kategori[nama_kategori] = 0
            pengeluaran_kategori[nama_kategori] += transaksi["nominal"]

    saldo = total_pemasukan - total_pengeluaran

    # Cari kategori dengan pengeluaran terbesar
    kategori_terbesar = "-"
    nominal_terbesar = 0
    for nama_kategori, jumlah in pengeluaran_kategori.items():
        if jumlah > nominal_terbesar:
            nominal_terbesar = jumlah
            kategori_terbesar = nama_kategori

    # Urutkan kategori dari pengeluaran terbesar ke terkecil
    urutan_kategori = list(pengeluaran_kategori.items())
    for i in range(len(urutan_kategori)):
        for j in range(i + 1, len(urutan_kategori)):
            if urutan_kategori[j][1] > urutan_kategori[i][1]:
                urutan_kategori[i], urutan_kategori[j] = urutan_kategori[j], urutan_kategori[i]

    # Hitung persentase tabungan (saving rate)
    if total_pemasukan > 0:
        persen_tabungan = ((total_pemasukan - total_pengeluaran) / total_pemasukan) * 100
        teks_tabungan = f"{persen_tabungan:.2f}%"
    else:
        teks_tabungan = "Tidak dapat dihitung (pemasukan Rp 0)"

    return {
        "bulan": bulan,
        "jumlah_transaksi": len(transaksi_bulan),
        "total_pemasukan": total_pemasukan,
        "total_pengeluaran": total_pengeluaran,
        "saldo": saldo,
        "urutan_kategori": urutan_kategori,
        "kategori_terbesar": kategori_terbesar,
        "nominal_terbesar": nominal_terbesar,
        "teks_tabungan": teks_tabungan,
    }


def tampilkan_laporan_bulanan(daftar_transaksi):
    """Menampilkan laporan keuangan bulanan ke terminal."""
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
    print(f"Persentase Tabungan (Saving) : {laporan['teks_tabungan']}")

    if laporan["kategori_terbesar"] != "-":
        print(f"Kategori Pengeluaran Terbesar: {laporan['kategori_terbesar']} ({format_rupiah(laporan['nominal_terbesar'])})")
    else:
        print("Kategori Pengeluaran Terbesar: Belum ada pengeluaran")

    print("\nRincian Pengeluaran per Kategori:")
    cetak_garis(panjang=52, karakter="-")
    if len(laporan["urutan_kategori"]) > 0:
        for nama_kategori, jumlah in laporan["urutan_kategori"]:
            persen = (jumlah / laporan["total_pengeluaran"]) * 100
            print(f"  {nama_kategori:<22} : {format_rupiah(jumlah):>14} ({persen:5.1f}%)")
    else:
        print("  (Tidak ada pengeluaran pada bulan ini)")
    cetak_garis()


# FITUR 4: EKSPOR DATA KE CSV
def menu_ekspor_csv(daftar_transaksi):
    """Sub-menu untuk mengekspor seluruh transaksi atau ringkasan bulanan ke CSV."""
    print()
    cetak_garis()
    print("EKSPOR DATA KE CSV")
    cetak_garis()
    print("1. Ekspor Semua Data Transaksi (ekspor_transaksi.csv)")
    print("2. Ekspor Ringkasan Keuangan Bulanan (ringkasan_bulanan_YYYY-MM.csv)")
    print("0. Kembali ke Menu Utama")

    pilihan = input("Pilih jenis ekspor (0-2): ").strip()
    if pilihan == "1":
        if len(daftar_transaksi) == 0:
            print("  [!] Belum ada data transaksi untuk diekspor.")
            return
        with open("ekspor_transaksi.csv", mode="w", encoding="utf-8", newline="") as file:
            penulis = csv.DictWriter(file, fieldnames=kolom_csv)
            penulis.writeheader()
            penulis.writerows(daftar_transaksi)
        print(f"[Sukses] {len(daftar_transaksi)} transaksi berhasil diekspor ke 'ekspor_transaksi.csv'.")

    elif pilihan == "2":
        bulan = input_bulan()
        laporan = hitung_laporan_bulanan(daftar_transaksi, bulan)
        nama_file = f"ringkasan_bulanan_{bulan}.csv"

        with open(nama_file, mode="w", encoding="utf-8", newline="") as file:
            penulis = csv.writer(file)
            penulis.writerow(["Ringkasan Keuangan Bulanan", bulan])
            penulis.writerow(["Metrik", "Nilai"])
            penulis.writerow(["Jumlah Transaksi", laporan["jumlah_transaksi"]])
            penulis.writerow(["Total Pemasukan", laporan["total_pemasukan"]])
            penulis.writerow(["Total Pengeluaran", laporan["total_pengeluaran"]])
            penulis.writerow(["Saldo Bulanan", laporan["saldo"]])
            penulis.writerow(["Kategori Pengeluaran Terbesar", laporan["kategori_terbesar"]])
            penulis.writerow(["Nominal Kategori Terbesar", laporan["nominal_terbesar"]])
            penulis.writerow(["Saving Rate", laporan["teks_tabungan"]])
            penulis.writerow([])

            penulis.writerow(["Rincian Pengeluaran per Kategori", "Nominal", "Persentase"])
            if len(laporan["urutan_kategori"]) > 0:
                for nama_kategori, jumlah in laporan["urutan_kategori"]:
                    persen = (jumlah / laporan["total_pengeluaran"]) * 100
                    penulis.writerow([nama_kategori, jumlah, f"{persen:.1f}%"])
            else:
                penulis.writerow(["Tidak ada pengeluaran", 0, "0.0%"])

        print(f"[Sukses] Ringkasan bulan {bulan} berhasil diekspor ke '{nama_file}'.")

    elif pilihan == "0":
        return
    else:
        print("  [!] Pilihan tidak valid.")


# FITUR 5: DASHBOARD
def tampilkan_dashboard(daftar_transaksi):
    """Menampilkan saldo total dan maksimal 5 transaksi terbaru."""
    total_pemasukan = 0
    total_pengeluaran = 0
    for transaksi in daftar_transaksi:
        if transaksi["jenis"] == "pemasukan":
            total_pemasukan += transaksi["nominal"]
        elif transaksi["jenis"] == "pengeluaran":
            total_pengeluaran += transaksi["nominal"]
    saldo = total_pemasukan - total_pengeluaran

    print()
    cetak_garis()
    print("SIMPLE PERSONAL FINANCE TRACKER - DASHBOARD")
    cetak_garis()
    print(f"Total Pemasukan   : {format_rupiah(total_pemasukan)}")
    print(f"Total Pengeluaran : {format_rupiah(total_pengeluaran)}")
    print(f"Saldo Saat Ini    : {format_rupiah(saldo)}")
    print(f"Jumlah Transaksi  : {len(daftar_transaksi)}")
    cetak_garis(karakter="-")
    print("5 Transaksi Terbaru:")

    if len(daftar_transaksi) == 0:
        print("  (Belum ada transaksi. Pilih menu 1 untuk mulai mencatat.)")
    else:
        transaksi_terbaru = daftar_transaksi[-5:][::-1]
        for transaksi in transaksi_terbaru:
            tanda = "+" if transaksi["jenis"] == "pemasukan" else "-"
            print(
                f"  [{transaksi['tanggal']}] {tanda} {format_rupiah(transaksi['nominal']):<13} "
                f"| {transaksi['kategori']:<13} | {transaksi['keterangan']}"
            )
    cetak_garis()


# PROGRAM UTAMA
def main():
    daftar_transaksi = panggil_aman("muat_transaksi", nama_file_data)
    if daftar_transaksi is None:
        daftar_transaksi = []

    try:
        while True:
            panggil_aman("tampilkan_dashboard", daftar_transaksi)
            print("MENU UTAMA:")
            print("  1. Tambah Transaksi (Pemasukan / Pengeluaran)")
            print("  2. Lihat & Filter Transaksi")
            print("  3. Laporan Keuangan Bulanan")
            print("  4. Ekspor Data ke CSV")
            print("  5. Keluar")

            pilihan = input("\nPilih menu (1-5): ").strip()

            if pilihan == "1":
                panggil_aman("tambah_transaksi", daftar_transaksi, nama_file_data)
            elif pilihan == "2":
                panggil_aman("menu_lihat_transaksi", daftar_transaksi)
            elif pilihan == "3":
                panggil_aman("tampilkan_laporan_bulanan", daftar_transaksi)
            elif pilihan == "4":
                panggil_aman("menu_ekspor_csv", daftar_transaksi)
            elif pilihan == "5":
                print("\nTerima kasih telah menggunakan Simple Personal Finance Tracker. Sampai jumpa!")
                break
            else:
                print("\n  [!] Pilihan menu tidak valid. Silakan pilih angka 1 sampai 5.")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C). Data yang sudah tersimpan tetap aman.")


if __name__ == "__main__":
    main()