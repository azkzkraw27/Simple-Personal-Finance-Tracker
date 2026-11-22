import csv
import os
from datetime import datetime

nama_file_data = "transaksi.csv"
kolom_csv = ["tanggal", "jenis", "kategori", "keterangan", "nominal"]

def format_rupiah(angka):
    tanda = "-" if angka < 0 else ""
    nilai_tetap = abs(int(round(angka)))
    format = f"{nilai_tetap:,}".replace(",", ".")
    return f"{tanda}Rp {format}"

def cetak_garis(panjang=82, karakter="="):
    print(karakter * panjang)
    
    
#ini masuk ke fungsi penyimpanan nyak dan membaca csv nya

def memuat_transaksi(nama_file=nama_file_data):
    
    daftar_transaksi = []
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
                    print(f"[Peringatan Sistem] Baris ke-{nomor_baris} pada '{nama_file}' tidak valid dan dilewati.")
    
    except FileNotFoundError:
        return []
    except OSError as error:
        print(f"[Error!] gagal membaca file '{nama_file}': {error}")
        return []
    
    return daftar_transaksi


#fungsi mengecek input pengguna

def input_tanggal():
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    while True:
        teks = input(f"Tanggal (Tahun-Bulan-Tanggal) [Tekan Enter {hari_ini}]: ").strip()
        if teks == "":
            return hari_ini
        try:
            datetime.strptime(teks, "%Y-%m-%d")
            return teks
        except ValueError:
            print("[Error!] Format Tanggal tidak Valid, Gunakan Format YYYY-MM-DD (Tahun-Bulan-Tanggal / contoh 2026-11-23).")
            
def input_jenis():
    while True:
        print("Pilih jenis transaksi")
        print("   1. Pemasukan")
        print("   2. Pengeluaran")
        pilihan = input("Masukkan Pilihan anda (1/2): ").strip().lower()
        if pilihan in ("1", "pemasukan"):
            return "pemasukan"
        if pilihan in ("2", "pengeluaran"):
            return "pengeluaran"
        print(" [Error!] Pilihan Tidak Valid. Ketik 1 untuk Pemasukan dan Ketik 2 untuk Pengeluaran.")
        
def input_teks_wajib(prompt):
    while True:
        nilai = input(prompt).strip()
        if nilai != "":
            return nilai
        print(" [Error!] Input tidak boleh kosong. Silahkan mengisi kembali.")
        
def input_nominal():
    while True:
        teks = input("Nominal (Rp, angka saja contoh 25000): ").strip()
        teks_bersih = teks.replace(".", "").replace(".", "")
        try:
            nominal = int(teks_bersih)
            if nominal <= 0:
                print(" [Error!] Nominal harus lebih besar dari 0.")
                continue
            return nominal
        except ValueError:
            print(" [Error!] Input tidak valid. Nominal harus berupa angka positif (contoh: 25000).")
        
def input_bulan():
    bulan_ini = datetime.now().strftime("%Y-%m")
    while True:
        teks = input(f"Masukkan bulan (YYYY-MM / Tahun-Bulan) [Enter untuk {bulan_ini}]: ").strip()
        if teks == "":
            return bulan_ini
        try:
            datetime.strptime(teks, "%Y-%m")
            return teks
        except ValueError:
            print(" [Error!] Format Bulan tidak valid. Gunakan format YYYY-MM / Tahun-Bulan (contoh: 2026-11)")
            
            
#fitur pertama yaitu manajemen transaksi (Menambah Data)

def tambah_transaksi(daftar_transaksi, nama_file=nama_file_data):
    print()
    cetak_garis()
    print("TAMBAH TRANSAKSI BARU")
    cetak_garis()
    
    tanggal = input_tanggal()
    jenis = input_jenis()
    kategori = input_teks_wajib("Kategori (cont. Makanan, Transport, Gaji, Uang Saku): ")
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
    
    print(f"\n[Berhasil!] Transaksi {jenis} sebesar {format_rupiah(nominal)} berhasil disimpan.")