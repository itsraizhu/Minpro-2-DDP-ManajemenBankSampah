import os
import pwinput
from prettytable import PrettyTable

USERS = {
    "admin": {"password": "admin123", "role": "admin", "nama": "Administrator"},
    "budi": {"password": "123", "role": "user", "nama": "Budi Santoso"}
}

HARGA_SAMPAH = {
    "1": {"nama": "Plastik", "poin_per_kg": 500},
    "2": {"nama": "Kertas", "poin_per_kg": 300},
    "3": {"nama": "Logam", "poin_per_kg": 1000},
    "4": {"nama": "Kaca", "poin_per_kg": 400}
}

data_setoran = [
    {"nama": "Budi Santoso", "jenis": "Plastik", "berat": 2.5, "poin": 1250, "user": "budi"}
]

def hapus_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_angka_positif(pesan):
    while True:
        try:
            nilai = float(input(pesan))
            if nilai <= 0:
                print("Input tidak boleh 0 atau minus!")
            else:
                return nilai
        except ValueError:
            print("Input harus berupa angka!")

def input_int_positif(pesan):
    while True:
        try:
            nilai = int(input(pesan))
            if nilai <= 0:
                print("Angka harus lebih dari 0!")
            else:
                return nilai
        except ValueError:
            print("Input harus berupa angka bulat!")

def pilih_jenis_sampah():
    print("PILIH JENIS SAMPAH")
    tabel = PrettyTable()
    tabel.field_names = ["Kode", "Jenis Sampah", "Poin / kg"]
    for kode in HARGA_SAMPAH:
        tabel.add_row([kode, HARGA_SAMPAH[kode]["nama"], HARGA_SAMPAH[kode]["poin_per_kg"]])
    print(tabel)
    while True:
        pilihan = input("Pilih kode jenis sampah (1-4): ")
        if pilihan in HARGA_SAMPAH:
            return HARGA_SAMPAH[pilihan]["nama"], HARGA_SAMPAH[pilihan]["poin_per_kg"]
        print("Pilihan tidak valid, pilih 1-4!")

def tambah_setoran(username_login, is_admin):
    print("TAMBAH SETORAN SAMPAH")
    if is_admin:
        nama_warga = input("Masukkan nama warga: ")
        if nama_warga == "":
            print("Nama tidak boleh kosong!")
            return
        pemilik = "admin"
    else:
        nama_warga = USERS[username_login]["nama"]
        pemilik = username_login
        print("Nama Nasabah:", nama_warga)

    jenis_nama, poin_rate = pilih_jenis_sampah()
    berat = input_angka_positif("Masukkan berat sampah (kg): ")
    poin_didapat = int(berat * poin_rate)

    data_baru = {
        "nama": nama_warga,
        "jenis": jenis_nama,
        "berat": berat,
        "poin": poin_didapat,
        "user": pemilik
    }
    data_setoran.append(data_baru)
    print("Data setoran berhasil ditambahkan!")

def lihat_setoran(username_filter=None):
    print("DAFTAR SETORAN SAMPAH")
    
    list_tampil = []
    if username_filter != None:
        for item in data_setoran:
            if item["user"] == username_filter:
                list_tampil.append(item)
    else:
        list_tampil = data_setoran

    if len(list_tampil) == 0:
        print("Belum ada data setoran.")
        return False

    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Warga", "Jenis Sampah", "Berat (kg)", "Poin"]
    
    total_berat = 0
    total_poin = 0
    nomor = 1

    for item in list_tampil:
        tabel.add_row([nomor, item["nama"], item["jenis"], item["berat"], item["poin"]])
        total_berat = total_berat + item["berat"]
        total_poin = total_poin + item["poin"]
        nomor = nomor + 1

    print(tabel)
    print("Total Berat :", total_berat, "kg")
    print("Total Poin  :", total_poin, "poin")
    return True

def ubah_setoran():
    if lihat_setoran() == False:
        return

    print("UBAH DATA SETORAN")
    nomor_input = input_int_positif("Masukkan nomor data yang ingin diubah: ")
    index = nomor_input - 1

    if index >= 0 and index < len(data_setoran):
        item = data_setoran[index]
        print("Mengubah data milik:", item["nama"])
        
        nama_baru = input("Masukkan nama baru (tekan Enter jika tidak diubah): ")
        if nama_baru != "":
            item["nama"] = nama_baru

        pilih_ubah_jenis = input("Ubah jenis sampah? (y/n): ")
        if pilih_ubah_jenis == "y":
            jenis_baru, poin_rate = pilih_jenis_sampah()
            item["jenis"] = jenis_baru
        else:
            poin_rate = 500
            for k in HARGA_SAMPAH:
                if HARGA_SAMPAH[k]["nama"] == item["jenis"]:
                    poin_rate = HARGA_SAMPAH[k]["poin_per_kg"]

        pilih_ubah_berat = input("Ubah berat sampah? (y/n): ")
        if pilih_ubah_berat == "y":
            item["berat"] = input_angka_positif("Masukkan berat baru (kg): ")

        item["poin"] = int(item["berat"] * poin_rate)
        print("Data berhasil diperbarui!")
    else:
        print("Nomor data tidak ditemukan!")

def hapus_setoran():
    if lihat_setoran() == False:
        return

    print("HAPUS DATA SETORAN")
    nomor_input = input_int_positif("Masukkan nomor data yang ingin dihapus: ")
    index = nomor_input - 1

    if index >= 0 and index < len(data_setoran):
        nama_terhapus = data_setoran[index]["nama"]
        del data_setoran[index]
        print("Data milik", nama_terhapus, "berhasil dihapus!")
    else:
        print("Nomor data tidak ditemukan!")

def login():
    hapus_layar()
    print("LOGIN SISTEM BANK SAMPAH")
    
    username = input("Masukkan Username : ")
    password = pwinput.pwinput("Masukkan Password : ")

    if username in USERS and USERS[username]["password"] == password:
        return username, USERS[username]["role"], USERS[username]["nama"]
    else:
        print("Username atau Password salah!")
        input("Tekan Enter untuk mencoba lagi...")
        return None, None, None

def menu_admin(username, nama):
    while True:
        print("MENU ADMIN BANK SAMPAH", nama)
        print("1. Tambah Setoran Sampah (Create)")
        print("2. Lihat Semua Data Setoran (Read)")
        print("3. Ubah Data Setoran (Update)")
        print("4. Hapus Data Setoran (Delete)")
        print("5. Logout")
        
        pilihan = input("Pilih menu (1-5): ")
        hapus_layar()
        
        if pilihan == "1":
            tambah_setoran(username, True)
        elif pilihan == "2":
            lihat_setoran()
        elif pilihan == "3":
            ubah_setoran()
        elif pilihan == "4":
            hapus_setoran()
        elif pilihan == "5":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan menu tidak valid!")

def menu_user(username, nama):
    while True:
        print("NASABAH / WARGA -", nama)
        print("1. Tambah Setoran Saya")
        print("2. Lihat Riwayat Setoran Saya")
        print("3. Lihat Daftar Poin Sampah")
        print("4. Logout")
        
        pilihan = input("Pilih menu (1-4): ")
        hapus_layar()
        
        if pilihan == "1":
            tambah_setoran(username, False)
        elif pilihan == "2":
            lihat_setoran(username)
        elif pilihan == "3":
            pilih_jenis_sampah()
        elif pilihan == "4":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan menu tidak valid!")

def main():
    while True:
        username, role, nama = login()
        if username != None:
            hapus_layar()
            print("Selamat datang,", nama)
            if role == "admin":
                menu_admin(username, nama)
            elif role == "user":
                menu_user(username, nama)

main()
