import csv
import os
from datetime import datetime

# ==============================================================================
# KONFIGURASI DASAR PROGRAM
# ==============================================================================
NAMA_FILE_DATA = "transaksi.csv"
KOLOM_CSV = ["tanggal", "jenis", "kategori", "keterangan", "nominal"]


# ==============================================================================
# 1. FUNGSI BANTUAN (UTILITY) - MANDIRI
# ==============================================================================
def format_rupiah(angka):
    """Mengubah angka (misal 25000) menjadi format Rupiah ('Rp 25.000')."""
    tanda = "-" if angka < 0 else ""
    nilai_bulat = abs(int(round(angka)))
    # Format dengan pemisah koma dulu, lalu ubah koma menjadi titik
    teks_angka = f"{nilai_bulat:,}".replace(",", ".")
    return f"{tanda}Rp {teks_angka}"


def cetak_garis(panjang=80, karakter="="):
    """Mencetak garis horizontal di terminal agar tampilan rapi."""
    print(karakter * panjang)


# ==============================================================================
# 2. FUNGSI BACA & SIMPAN FILE CSV - MANDIRI
# ==============================================================================
def muat_transaksi(nama_file=NAMA_FILE_DATA):
    """Membaca data dari file CSV ke dalam list of dictionary."""
    daftar_transaksi = []

    # Jika file CSV belum ada (pemakaian pertama kali), kembalikan list kosong
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

                    # Pastikan tanggal valid dan nominal lebih dari 0
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
                    print(f"[Peringatan] Baris ke-{nomor_baris} pada '{nama_file}' dilewati karena tidak valid.")
    except OSError as error:
        print(f"[Error] Gagal membaca file '{nama_file}': {error}")

    return daftar_transaksi


def simpan_transaksi(transaksi, nama_file=NAMA_FILE_DATA):
    """Menambahkan 1 transaksi baru ke baris paling bawah file CSV."""
    file_baru = (not os.path.exists(nama_file)) or (os.path.getsize(nama_file) == 0)

    # Mode 'a' (append) menambah baris baru tanpa menghapus isi file lama
    with open(nama_file, mode="a", encoding="utf-8", newline="") as file:
        penulis = csv.DictWriter(file, fieldnames=KOLOM_CSV)
        if file_baru:
            penulis.writeheader()
        penulis.writerow(transaksi)


# ==============================================================================
# 3. FUNGSI VALIDASI INPUT PENGGUNA - MANDIRI
# ==============================================================================
def input_tanggal():
    """Meminta tanggal YYYY-MM-DD. Jika langsung Enter, pakai tanggal hari ini."""
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
    """Meminta pengguna memilih pemasukan atau pengeluaran."""
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
    """Meminta teks yang tidak boleh kosong."""
    while True:
        nilai = input(pesan).strip()
        if nilai != "":
            return nilai
        print("  [!] Input tidak boleh kosong. Silakan isi lagi.")


def input_nominal():
    """Meminta nominal uang berupa angka bulat positif (> 0)."""
    while True:
        teks = input("Nominal (Rp, angka saja mis. 25000): ").strip()
        teks_bersih = teks.replace(".", "").replace(",", "")
        try:
            nominal = int(teks_bersih)
            if nominal <= 0:
                print("  [!] Nominal harus lebih besar dari 0.")
                continue
            return nominal
        except ValueError:
            print("  [!] Input tidak valid. Masukkan angka positif (contoh: 25000).")


def input_bulan():
    """Meminta input bulan YYYY-MM. Jika langsung Enter, pakai bulan sekarang."""
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


# ==============================================================================
# 4. FITUR 1: TAMBAH TRANSAKSI (MANDIRI - TIDAK BERGANTUNG FUNGSI LAIN)
# ==============================================================================
def tambah_transaksi(daftar_transaksi, nama_file=NAMA_FILE_DATA):
    """Menambah transaksi baru ke CSV dan list di memori secara mandiri."""
    print()
    print("=" * 80)
    print("TAMBAH TRANSAKSI BARU")
    print("=" * 80)

    # 1. Input & validasi tanggal
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    while True:
        tanggal = input(f"Tanggal (YYYY-MM-DD) [Enter untuk {hari_ini}]: ").strip()
        if tanggal == "":
            tanggal = hari_ini
            break
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            break
        except ValueError:
            print("  [!] Format tanggal salah. Contoh: 2026-11-15")

    # 2. Input & validasi jenis transaksi
    while True:
        print("Pilih jenis transaksi:")
        print("  1. Pemasukan")
        print("  2. Pengeluaran")
        pilihan_jenis = input("Masukkan pilihan (1/2): ").strip().lower()
        if pilihan_jenis in ("1", "pemasukan"):
            jenis = "pemasukan"
            break
        elif pilihan_jenis in ("2", "pengeluaran"):
            jenis = "pengeluaran"
            break
        else:
            print("  [!] Ketik 1 untuk Pemasukan atau 2 untuk Pengeluaran.")

    # 3. Input kategori wajib
    while True:
        kategori = input("Kategori (mis. Makanan, Kost, Transport, Uang Saku): ").strip()
        if kategori != "":
            break
        print("  [!] Kategori tidak boleh kosong.")

    # 4. Input keterangan wajib
    while True:
        keterangan = input("Keterangan singkat: ").strip()
        if keterangan != "":
            break
        print("  [!] Keterangan tidak boleh kosong.")

    # 5. Input nominal positif
    while True:
        teks_nominal = input("Nominal (Rp, angka saja mis. 25000): ").strip()
        teks_bersih = teks_nominal.replace(".", "").replace(",", "")
        try:
            nominal = int(teks_bersih)
            if nominal > 0:
                break
            print("  [!] Nominal harus lebih besar dari 0.")
        except ValueError:
            print("  [!] Nominal harus berupa angka positif (contoh: 25000).")

    transaksi_baru = {
        "tanggal": tanggal,
        "jenis": jenis,
        "kategori": kategori,
        "keterangan": keterangan,
        "nominal": nominal,
    }

    # Simpan langsung ke CSV
    file_baru = (not os.path.exists(nama_file)) or (os.path.getsize(nama_file) == 0)
    with open(nama_file, mode="a", encoding="utf-8", newline="") as file:
        penulis = csv.DictWriter(file, fieldnames=KOLOM_CSV)
        if file_baru:
            penulis.writeheader()
        penulis.writerow(transaksi_baru)

    daftar_transaksi.append(transaksi_baru)
    nominal_rp = f"Rp {nominal:,}".replace(",", ".")
    print(f"\n[Sukses] Transaksi {jenis} sebesar {nominal_rp} berhasil disimpan.")


# ==============================================================================
# 5. FITUR 2: LIHAT & FILTER TRANSAKSI (MANDIRI)
# ==============================================================================
def filter_transaksi(daftar_transaksi, jenis_filter=None):
    """Menyaring transaksi berdasarkan jenis ('pemasukan' atau 'pengeluaran')."""
    if jenis_filter is None:
        return list(daftar_transaksi)
    hasil = []
    for trx in daftar_transaksi:
        if trx["jenis"] == jenis_filter:
            hasil.append(trx)
    return hasil


def tampilkan_tabel_transaksi(daftar_transaksi, judul="DAFTAR TRANSAKSI"):
    """Mencetak daftar transaksi dalam bentuk tabel rapi secara mandiri."""
    print()
    print("=" * 80)
    print(judul)
    print("=" * 80)

    if len(daftar_transaksi) == 0:
        print("Belum ada data transaksi yang sesuai.")
        print("=" * 80)
        return

    print(f"{'No':<4} {'Tanggal':<12} {'Jenis':<13} {'Kategori':<15} {'Keterangan':<20} {'Nominal':>12}")
    print("-" * 80)

    total = 0
    for nomor, trx in enumerate(daftar_transaksi, start=1):
        ket = trx["keterangan"]
        if len(ket) > 19:
            ket = ket[:16] + "..."

        kat = trx["kategori"]
        if len(kat) > 14:
            kat = kat[:11] + "..."

        nominal_rp = f"Rp {trx['nominal']:,}".replace(",", ".")
        print(f"{nomor:<4} {trx['tanggal']:<12} {trx['jenis']:<13} {kat:<15} {ket:<20} {nominal_rp:>12}")
        total += trx["nominal"]

    total_rp = f"Rp {total:,}".replace(",", ".")
    print("-" * 80)
    print(f"Total transaksi ditampilkan: {len(daftar_transaksi)} | Jumlah nominal: {total_rp}")
    print("=" * 80)


def menu_lihat_transaksi(daftar_transaksi):
    """Sub-menu lihat & filter transaksi yang berjalan mandiri."""
    print()
    print("=" * 80)
    print("LIHAT & FILTER TRANSAKSI")
    print("=" * 80)
    print("1. Tampilkan Semua Transaksi")
    print("2. Filter: Hanya Pemasukan")
    print("3. Filter: Hanya Pengeluaran")
    print("0. Kembali ke Menu Utama")

    pilihan = input("Pilih tampilan (0-3): ").strip()
    if pilihan == "1":
        data_tampil = list(daftar_transaksi)
        judul = "SEMUA TRANSAKSI"
    elif pilihan == "2":
        data_tampil = [trx for trx in daftar_transaksi if trx["jenis"] == "pemasukan"]
        judul = "TRANSAKSI PEMASUKAN"
    elif pilihan == "3":
        data_tampil = [trx for trx in daftar_transaksi if trx["jenis"] == "pengeluaran"]
        judul = "TRANSAKSI PENGELUARAN"
    elif pilihan == "0":
        return
    else:
        print("  [!] Pilihan tidak valid.")
        return

    print()
    print("=" * 80)
    print(judul)
    print("=" * 80)
    if len(data_tampil) == 0:
        print("Belum ada data transaksi yang sesuai.")
        print("=" * 80)
        return

    print(f"{'No':<4} {'Tanggal':<12} {'Jenis':<13} {'Kategori':<15} {'Keterangan':<20} {'Nominal':>12}")
    print("-" * 80)
    total = 0
    for nomor, trx in enumerate(data_tampil, start=1):
        ket = trx["keterangan"][:16] + "..." if len(trx["keterangan"]) > 19 else trx["keterangan"]
        kat = trx["kategori"][:11] + "..." if len(trx["kategori"]) > 14 else trx["kategori"]
        nominal_rp = f"Rp {trx['nominal']:,}".replace(",", ".")
        print(f"{nomor:<4} {trx['tanggal']:<12} {trx['jenis']:<13} {kat:<15} {ket:<20} {nominal_rp:>12}")
        total += trx["nominal"]
    total_rp = f"Rp {total:,}".replace(",", ".")
    print("-" * 80)
    print(f"Total transaksi ditampilkan: {len(data_tampil)} | Jumlah nominal: {total_rp}")
    print("=" * 80)


# ==============================================================================
# 6. FITUR 3: LAPORAN KEUANGAN BULANAN (MANDIRI)
# ==============================================================================
def hitung_laporan_bulanan(daftar_transaksi, bulan):
    """Menghitung ringkasan keuangan satu bulan (YYYY-MM)."""
    transaksi_bulan = []
    for trx in daftar_transaksi:
        if trx["tanggal"].startswith(bulan):
            transaksi_bulan.append(trx)

    total_pemasukan = 0
    total_pengeluaran = 0
    pengeluaran_per_kategori = {}

    for trx in transaksi_bulan:
        if trx["jenis"] == "pemasukan":
            total_pemasukan += trx["nominal"]
        elif trx["jenis"] == "pengeluaran":
            total_pengeluaran += trx["nominal"]
            kat = trx["kategori"]
            if kat not in pengeluaran_per_kategori:
                pengeluaran_per_kategori[kat] = 0
            pengeluaran_per_kategori[kat] += trx["nominal"]

    saldo = total_pemasukan - total_pengeluaran

    kategori_terbesar = "-"
    nominal_terbesar = 0
    for kat, jumlah in pengeluaran_per_kategori.items():
        if jumlah > nominal_terbesar:
            nominal_terbesar = jumlah
            kategori_terbesar = kat

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
    """Menampilkan laporan keuangan bulanan ke terminal secara mandiri."""
    print()
    print("=" * 80)
    print("LAPORAN KEUANGAN BULANAN")
    print("=" * 80)

    bulan_ini = datetime.now().strftime("%Y-%m")
    while True:
        bulan = input(f"Masukkan bulan (YYYY-MM) [Enter untuk {bulan_ini}]: ").strip()
        if bulan == "":
            bulan = bulan_ini
            break
        try:
            datetime.strptime(bulan, "%Y-%m")
            break
        except ValueError:
            print("  [!] Format bulan salah. Contoh: 2026-11")

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
            pengeluaran_per_kategori[kat] = pengeluaran_per_kategori.get(kat, 0) + trx["nominal"]

    saldo = total_pemasukan - total_pengeluaran

    print()
    print("=" * 80)
    print(f"RINGKASAN KEUANGAN BULAN {bulan}")
    print("=" * 80)

    if len(transaksi_bulan) == 0:
        print(f"Tidak ditemukan transaksi pada bulan {bulan}.")
        print("=" * 80)
        return

    if total_pemasukan > 0:
        saving_rate = ((total_pemasukan - total_pengeluaran) / total_pemasukan) * 100
        saving_teks = f"{saving_rate:.2f}%"
    else:
        saving_teks = "Tidak dapat dihitung (pemasukan Rp 0)"

    kategori_terbesar = "-"
    nominal_terbesar = 0
    for kat, jumlah in pengeluaran_per_kategori.items():
        if jumlah > nominal_terbesar:
            nominal_terbesar = jumlah
            kategori_terbesar = kat

    def rp(nilai):
        tanda = "-" if nilai < 0 else ""
        return f"{tanda}Rp {abs(int(round(nilai))):,}".replace(",", ".")

    print(f"Jumlah Transaksi             : {len(transaksi_bulan)}")
    print(f"Total Pemasukan              : {rp(total_pemasukan)}")
    print(f"Total Pengeluaran            : {rp(total_pengeluaran)}")
    print(f"Saldo Bulanan                : {rp(saldo)}")
    print(f"Persentase Tabungan (Saving) : {saving_teks}")

    if kategori_terbesar != "-":
        print(f"Kategori Pengeluaran Terbesar: {kategori_terbesar} ({rp(nominal_terbesar)})")
    else:
        print("Kategori Pengeluaran Terbesar: Belum ada pengeluaran")

    print("\nRincian Pengeluaran per Kategori:")
    print("-" * 52)
    if len(pengeluaran_per_kategori) > 0:
        daftar_kat = list(pengeluaran_per_kategori.items())
        for i in range(len(daftar_kat)):
            for j in range(i + 1, len(daftar_kat)):
                if daftar_kat[j][1] > daftar_kat[i][1]:
                    daftar_kat[i], daftar_kat[j] = daftar_kat[j], daftar_kat[i]

        for kat, jumlah in daftar_kat:
            persen = (jumlah / total_pengeluaran) * 100
            print(f"  {kat:<22} : {rp(jumlah):>14} ({persen:5.1f}%)")
    else:
        print("  (Tidak ada pengeluaran pada bulan ini)")
    print("=" * 80)


# ==============================================================================
# 7. FITUR 4: EKSPOR DATA KE CSV (MANDIRI)
# ==============================================================================
def ekspor_data_transaksi(daftar_transaksi, nama_file="ekspor_transaksi.csv"):
    """Mengekspor seluruh data transaksi ke file CSV baru."""
    with open(nama_file, mode="w", encoding="utf-8", newline="") as file:
        penulis = csv.DictWriter(file, fieldnames=KOLOM_CSV)
        penulis.writeheader()
        penulis.writerows(daftar_transaksi)
    print(f"[Sukses] {len(daftar_transaksi)} transaksi berhasil diekspor ke '{nama_file}'.")


def ekspor_ringkasan_bulanan(daftar_transaksi, bulan, nama_file=None):
    """Mengekspor ringkasan keuangan bulanan ke file CSV."""
    if nama_file is None:
        nama_file = f"ringkasan_bulanan_{bulan}.csv"

    transaksi_bulan = [trx for trx in daftar_transaksi if trx["tanggal"].startswith(bulan)]
    total_pemasukan = sum(t["nominal"] for t in transaksi_bulan if t["jenis"] == "pemasukan")
    total_pengeluaran = sum(t["nominal"] for t in transaksi_bulan if t["jenis"] == "pengeluaran")
    saldo = total_pemasukan - total_pengeluaran

    per_kat = {}
    for t in transaksi_bulan:
        if t["jenis"] == "pengeluaran":
            per_kat[t["kategori"]] = per_kat.get(t["kategori"], 0) + t["nominal"]

    kat_max = "-"
    nom_max = 0
    for k, v in per_kat.items():
        if v > nom_max:
            nom_max = v
            kat_max = k

    if total_pemasukan > 0:
        sr = f"{((total_pemasukan - total_pengeluaran) / total_pemasukan) * 100:.2f}%"
    else:
        sr = "Tidak dapat dihitung (pemasukan Rp 0)"

    with open(nama_file, mode="w", encoding="utf-8", newline="") as file:
        penulis = csv.writer(file)
        penulis.writerow(["Ringkasan Keuangan Bulanan", bulan])
        penulis.writerow(["Metrik", "Nilai"])
        penulis.writerow(["Jumlah Transaksi", len(transaksi_bulan)])
        penulis.writerow(["Total Pemasukan", total_pemasukan])
        penulis.writerow(["Total Pengeluaran", total_pengeluaran])
        penulis.writerow(["Saldo Bulanan", saldo])
        penulis.writerow(["Kategori Pengeluaran Terbesar", kat_max])
        penulis.writerow(["Nominal Kategori Terbesar", nom_max])
        penulis.writerow(["Saving Rate", sr])
        penulis.writerow([])

        penulis.writerow(["Rincian Pengeluaran per Kategori", "Nominal", "Persentase"])
        if len(per_kat) > 0:
            daftar_kat = list(per_kat.items())
            for i in range(len(daftar_kat)):
                for j in range(i + 1, len(daftar_kat)):
                    if daftar_kat[j][1] > daftar_kat[i][1]:
                        daftar_kat[i], daftar_kat[j] = daftar_kat[j], daftar_kat[i]
            for kat, jumlah in daftar_kat:
                persen = (jumlah / total_pengeluaran) * 100
                penulis.writerow([kat, jumlah, f"{persen:.1f}%"])
        else:
            penulis.writerow(["Tidak ada pengeluaran", 0, "0.0%"])

    print(f"[Sukses] Ringkasan bulan {bulan} berhasil diekspor ke '{nama_file}'.")


def menu_ekspor_csv(daftar_transaksi):
    """Sub-menu ekspor CSV yang berjalan mandiri."""
    print()
    print("=" * 80)
    print("EKSPOR DATA KE CSV")
    print("=" * 80)
    print("1. Ekspor Semua Data Transaksi (ekspor_transaksi.csv)")
    print("2. Ekspor Ringkasan Keuangan Bulanan (ringkasan_bulanan_YYYY-MM.csv)")
    print("0. Kembali ke Menu Utama")

    pilihan = input("Pilih jenis ekspor (0-2): ").strip()
    if pilihan == "1":
        if len(daftar_transaksi) == 0:
            print("  [!] Belum ada data transaksi untuk diekspor.")
            return
        with open("ekspor_transaksi.csv", mode="w", encoding="utf-8", newline="") as file:
            penulis = csv.DictWriter(file, fieldnames=KOLOM_CSV)
            penulis.writeheader()
            penulis.writerows(daftar_transaksi)
        print(f"[Sukses] {len(daftar_transaksi)} transaksi berhasil diekspor ke 'ekspor_transaksi.csv'.")
    elif pilihan == "2":
        bulan_ini = datetime.now().strftime("%Y-%m")
        while True:
            bulan = input(f"Masukkan bulan (YYYY-MM) [Enter untuk {bulan_ini}]: ").strip()
            if bulan == "":
                bulan = bulan_ini
                break
            try:
                datetime.strptime(bulan, "%Y-%m")
                break
            except ValueError:
                print("  [!] Format bulan salah. Contoh: 2026-11")

        nama_file = f"ringkasan_bulanan_{bulan}.csv"
        transaksi_bulan = [trx for trx in daftar_transaksi if trx["tanggal"].startswith(bulan)]
        total_masuk = sum(t["nominal"] for t in transaksi_bulan if t["jenis"] == "pemasukan")
        total_keluar = sum(t["nominal"] for t in transaksi_bulan if t["jenis"] == "pengeluaran")
        saldo = total_masuk - total_keluar

        per_kat = {}
        for t in transaksi_bulan:
            if t["jenis"] == "pengeluaran":
                per_kat[t["kategori"]] = per_kat.get(t["kategori"], 0) + t["nominal"]

        kat_max = "-"
        nom_max = 0
        for k, v in per_kat.items():
            if v > nom_max:
                nom_max = v
                kat_max = k

        sr = f"{((total_masuk - total_keluar) / total_masuk) * 100:.2f}%" if total_masuk > 0 else "Tidak dapat dihitung (pemasukan Rp 0)"

        with open(nama_file, mode="w", encoding="utf-8", newline="") as file:
            penulis = csv.writer(file)
            penulis.writerow(["Ringkasan Keuangan Bulanan", bulan])
            penulis.writerow(["Metrik", "Nilai"])
            penulis.writerow(["Jumlah Transaksi", len(transaksi_bulan)])
            penulis.writerow(["Total Pemasukan", total_masuk])
            penulis.writerow(["Total Pengeluaran", total_keluar])
            penulis.writerow(["Saldo Bulanan", saldo])
            penulis.writerow(["Kategori Pengeluaran Terbesar", kat_max])
            penulis.writerow(["Nominal Kategori Terbesar", nom_max])
            penulis.writerow(["Saving Rate", sr])
            penulis.writerow([])
            penulis.writerow(["Rincian Pengeluaran per Kategori", "Nominal", "Persentase"])
            if len(per_kat) > 0:
                daftar_kat = sorted(per_kat.items(), key=lambda x: x[1], reverse=True)
                for kat, jumlah in daftar_kat:
                    persen = (jumlah / total_keluar) * 100
                    penulis.writerow([kat, jumlah, f"{persen:.1f}%"])
            else:
                penulis.writerow(["Tidak ada pengeluaran", 0, "0.0%"])
        print(f"[Sukses] Ringkasan bulan {bulan} berhasil diekspor ke '{nama_file}'.")
    elif pilihan == "0":
        return
    else:
        print("  [!] Pilihan tidak valid.")


# ==============================================================================
# 8. FITUR 5: DASHBOARD RINGKAS (MANDIRI)
# ==============================================================================
def tampilkan_dashboard(daftar_transaksi):
    """Menampilkan saldo total dan 5 transaksi terbaru secara mandiri."""
    total_masuk = 0
    total_keluar = 0
    for trx in daftar_transaksi:
        if trx["jenis"] == "pemasukan":
            total_masuk += trx["nominal"]
        elif trx["jenis"] == "pengeluaran":
            total_keluar += trx["nominal"]
    saldo = total_masuk - total_keluar

    def rp(nilai):
        tanda = "-" if nilai < 0 else ""
        return f"{tanda}Rp {abs(int(round(nilai))):,}".replace(",", ".")

    print()
    print("=" * 80)
    print("SIMPLE PERSONAL FINANCE TRACKER - DASHBOARD")
    print("=" * 80)
    print(f"Total Pemasukan   : {rp(total_masuk)}")
    print(f"Total Pengeluaran : {rp(total_keluar)}")
    print(f"Saldo Saat Ini    : {rp(saldo)}")
    print(f"Jumlah Transaksi  : {len(daftar_transaksi)}")
    print("-" * 80)
    print("5 Transaksi Terbaru:")

    if len(daftar_transaksi) == 0:
        print("  (Belum ada transaksi. Pilih menu 1 untuk mulai mencatat.)")
    else:
        terbaru = daftar_transaksi[-5:][::-1]
        for trx in terbaru:
            tanda = "+" if trx["jenis"] == "pemasukan" else "-"
            print(
                f"  [{trx['tanggal']}] {tanda} {rp(trx['nominal']):<13} "
                f"| {trx['kategori']:<13} | {trx['keterangan']}"
            )
    print("=" * 80)


# ==============================================================================
# 9. PROGRAM UTAMA (AMAN JIKA SALAH SATU FUNGSI DIHAPUS)
# ==============================================================================
def panggil_aman(nama_fungsi, *args):
    """Mengecek apakah fungsi masih ada sebelum dipanggil agar tidak NameError."""
    fungsi = globals().get(nama_fungsi)
    if callable(fungsi):
        return fungsi(*args)
    else:
        print(f"\n[Info] Fitur '{nama_fungsi}' sedang dinonaktifkan/dihapus.")
        return None


def main():
    """Titik masuk utama aplikasi dengan perlindungan jika fungsi fitur dihapus."""
    if callable(globals().get("muat_transaksi")):
        daftar_transaksi = muat_transaksi(NAMA_FILE_DATA)
    else:
        daftar_transaksi = []
        if os.path.exists(NAMA_FILE_DATA):
            with open(NAMA_FILE_DATA, mode="r", encoding="utf-8", newline="") as file:
                for baris in csv.DictReader(file):
                    try:
                        daftar_transaksi.append({
                            "tanggal": baris["tanggal"].strip(),
                            "jenis": baris["jenis"].strip().lower(),
                            "kategori": baris["kategori"].strip(),
                            "keterangan": baris["keterangan"].strip(),
                            "nominal": int(float(baris["nominal"].strip())),
                        })
                    except Exception:
                        pass

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
                panggil_aman("tambah_transaksi", daftar_transaksi, NAMA_FILE_DATA)
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
