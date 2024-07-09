import csv
import os
import time
import sys
from datetime import datetime
from colorama import init, Fore
from prettytable import PrettyTable
from pyfiglet import Figlet

def loading_page(seconds):
    animation = "|/-\\"
    for _ in range(seconds * 10):
        sys.stdout.write("\r" + Fore.BLUE + "=============== Loading =============" + animation[_ % len(animation)])
        sys.stdout.flush()
        time.sleep(0.1)
    os.system('cls')

class Obat:
    def __init__(self, nama, kondisi_kesehatan, kategori, stok, harga, terjual=0):
        self.nama = nama
        self.kondisi_kesehatan = kondisi_kesehatan
        self.kategori = kategori
        self.stok = int(stok)
        self.harga = int(harga)
        self.terjual = int(terjual) if terjual else 0

class Transaksi:
    def __init__(self, tanggal, nama, jumlah_beli, harga, subtotal, no_transaksi):
        self.tanggal = tanggal
        self.nama = nama
        self.harga = int(harga)
        self.jumlah_beli = int(jumlah_beli)
        self.subtotal = int(subtotal)
        self.no_transaksi = int(no_transaksi)

def register_user(obat_list):
    print(Fore.YELLOW + "=========================================")
    print(Fore.CYAN +   "                REGISTER                 ")
    print(Fore.YELLOW + "=========================================")
    username = input(Fore.YELLOW + "Masukkan username baru: ")
    password = input(Fore.YELLOW + "Masukkan password baru: ")
    add_user(username, password)
    print(Fore.YELLOW + "Register berhasil.")
    os.system('cls')
    user_menu(obat_list)

def login_user():
    os.system('cls')
    print(Fore.YELLOW + "=========================================")
    print(Fore.CYAN +   "                LOGIN                    ")
    print(Fore.YELLOW + "=========================================")
    username = input(Fore.YELLOW + "Masukkan username: ")
    password = input(Fore.YELLOW + "Masukkan password: ")
    if check_user(username, password):
        print(Fore.YELLOW + "Login berhasil.")
        return True
        os.system('cls')
    else:
        print(Fore.RED + "Username atau password salah.")
        return False

def register_or_login_user(obat_list):
    os.system('cls')
    print(Fore.BLUE + "=========================================")
    print(Fore.BLUE + "1. Login")
    print(Fore.BLUE + "2. Register")
    print(Fore.BLUE + "=========================================")
    choice = input(Fore.BLUE +"Masukkan pilihan Anda (1/2): ")
    os.system('cls') 

    if choice == '1': 
        os.system('cls')
        if login_user():
            os.system('cls')
            user_menu(obat_list)
        
    elif choice == '2':  
        os.system('cls')
        if register_user(obat_list):
            os.system('cls')
            user_menu(obat_list)
    else:
        print(Fore.RED + "Pilihan tidak valid. Silakan pilih kembali.")
        os.system('cls')

def add_admin(username, password):
    with open('admin.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

def add_user(username, password):
    with open('user.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

def check_admin(username, password):
    with open('admin.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

def check_user(username, password):
    with open('user.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

def tambah_obat(obat_list):
    print(Fore.YELLOW + "=========================================")
    print(Fore.YELLOW + "            TAMBAH OBAT                  ")
    print(Fore.YELLOW + "=========================================")
    nama = input(Fore.YELLOW + "Masukkan nama obat: ").strip().capitalize()

    obat_ditemukan = False
    for obat in obat_list:
        if obat.nama == nama:
            print(Fore.RED + f"Nama obat '{nama}' sudah ada.")
            pilihan = input(Fore.YELLOW + "Apakah Anda ingin menambah stok? (y/n): ").strip().lower()
            if pilihan == 'y':
                stok_tambahan = int(input(Fore.YELLOW + "Masukkan jumlah stok yang ingin ditambahkan: "))
                obat.stok += stok_tambahan
                print(Fore.BLUE + "Stok obat berhasil ditambahkan.")
                obat_ditemukan = True
                break
            elif pilihan == 'n':
                return
            else:
                print(Fore.RED + "Pilihan tidak valid. Operasi dibatalkan.")
                return
            

    if not obat_ditemukan:
        kondisi_kesehatan = input(Fore.YELLOW + "Masukkan kondisi kesehatan obat: ").strip().capitalize()
        kategori = input(Fore.YELLOW + "Masukkan kategori obat: ").strip().capitalize()
        stok = int(input(Fore.YELLOW + "Masukkan jumlah stok obat: ").strip())
        harga = input(Fore.YELLOW + "Masukkan harga obat: ").strip()
        obat_baru = Obat(nama, kondisi_kesehatan, kategori, stok, harga, terjual=0)
        obat_list.append(obat_baru)
        print(Fore.BLUE + "Obat baru berhasil ditambahkan.")


    write_obat('obat.csv', obat_list)

def read_obat(filename):
    obat_list = []
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            terjual = row.get('terjual', 0)
            obat_list.append(Obat(row['nama'].capitalize(), row['kondisi_kesehatan'].capitalize(), 
            row['kategori'].capitalize(), row['stok'], row['harga'], terjual))
    return obat_list

def write_obat(filename, obat_list):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['nama', 'kondisi_kesehatan', 'kategori', 'stok', 'harga', 'terjual']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for obat in obat_list:
            writer.writerow({'nama': obat.nama, 'kondisi_kesehatan': obat.kondisi_kesehatan, 'kategori': obat.kategori, 
                             'stok': obat.stok, 'harga': obat.harga, 'terjual': obat.terjual})


def hapus_obat(obat_list):
    print(Fore.CYAN + "=========================================")
    print(Fore.CYAN + "            HAPUS OBAT                   ")
    print(Fore.CYAN + "=========================================")
    nama_obat = input(Fore.CYAN + "Masukkan nama obat yang ingin dihapus: ").strip().capitalize()  
    found = False
    for obat in obat_list:
        if obat.nama == nama_obat:
            obat_list.remove(obat)
            write_obat('obat.csv', obat_list)
            found = True
            print(Fore.RED + "Obat berhasil dihapus.")
            break
    if not found:
        print(Fore.RED + "Obat tidak ditemukan.")


def add_transaksi_to_csv(filename, transaksi_data):
    new_kode_transaksi = 1  

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            transaksi_ada = list(reader)
            if transaksi_ada:  
                last_transaksi = transaksi_ada[-1]
                last_kode_transaksi = int(last_transaksi[-1])  
                new_kode_transaksi = last_kode_transaksi + 1  

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        for data in transaksi_data:
            data.append(new_kode_transaksi)
            writer.writerow(data)

def read_transaksi(filename):
    transaksi_list = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transaksi_list.append(Transaksi(row['tanggal'], row['nama'], row['jumlah_beli'], row['harga'], row['subtotal'], row['no_transaksi']))
    return transaksi_list

def display_riwayat_transaksi(transaksi_list, tanggal=None):
    print(Fore.YELLOW + "=========================================")
    print(Fore.BLUE + "      TAMPILKAN RIWAYAT TRANSAKSI          ")
    print(Fore.YELLOW + "=========================================")
    if not transaksi_list:
        print(Fore.RED + "Belum ada riwayat transaksi.")
    else:
        print(Fore.MAGENTA + "Riwayat Transaksi:")

        if tanggal:
            transaksi_list = [transaksi for transaksi in transaksi_list if transaksi.tanggal.split()[0] == tanggal]
        
        if not transaksi_list:
            print(f"Tidak ada transaksi pada tanggal {tanggal}.")
            return
        
        group_transaksi = {}
        for transaksi in transaksi_list:
            if transaksi.no_transaksi not in group_transaksi:
                group_transaksi[transaksi.no_transaksi] = []
            group_transaksi[transaksi.no_transaksi].append(transaksi)
        
        for no_transaksi, transaksi_group in group_transaksi.items():
            print(Fore.CYAN + " " * 25 + "E-PHARMACY")
            print(Fore.CYAN + " " * 22 + "STRUK PEMBELIAN")
            print(Fore.GREEN + "No. Transaksi:", no_transaksi)
            print(Fore.GREEN + "Tanggal Transaksi:", transaksi_group[0].tanggal)  
            print(Fore.YELLOW + "{:<20} | {:<10} | {:<10} | {:<10}".format("Nama Barang", "Qty", "Harga", "Sub Total"))
            print(Fore.YELLOW + "-" * 60)
            total_harga = 0
            for detail_transaksi in transaksi_group:
                total_harga += int(detail_transaksi.subtotal)
                print(Fore.WHITE + "{:<20} | {:<10} | {:<10} | {:<10}".format(detail_transaksi.nama, detail_transaksi.jumlah_beli, detail_transaksi.harga, detail_transaksi.subtotal))
            print(Fore.YELLOW + "-" * 60)
            print(Fore.WHITE + "{:<20} | {:<10} | {:<10} | {:<10}".format("TOTAL :", "", "", total_harga))
            print(Fore.YELLOW + "=" * 60)

def display_obat_info(obat):
    table = PrettyTable(["Nama", "Kondisi Kesehatan", "Kategori", "Stok", "Harga (Rp.)"])
    table.add_row([obat.nama, obat.kondisi_kesehatan, obat.kategori, obat.stok, obat.harga])
    print(table)

def display_all_obat(obat_list):
    merge_sort(obat_list, 'nama')
    table = PrettyTable(["Nama", "Harga (Rp.)"])
    table.align["Nama"] = "l" 
    for obat in obat_list:
        table.add_row([obat.nama, obat.harga])
    print(table)

def merge_sort(arr, key):
    if len(arr) > 1:
        mid = len(arr) // 2 
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half, key)
        merge_sort(right_half, key)

        i = j = k = 0 

        while i < len(left_half) and j < len(right_half):
            if getattr(left_half[i], key) < getattr(right_half[j], key):
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def binary_search(arr, key, value):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if getattr(arr[mid], key) == value: 
            return mid
        elif getattr(arr[mid], key) < value:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def beli_obat(obat_list):
    pembelian_list = []
    print(Fore.BLUE + "=========================================")
    print(Fore.YELLOW + "            BELI OBAT                  ")
    print(Fore.BLUE + "=========================================")
    while True:
        display_all_obat(obat_list) 
        nama_obat = input(Fore.YELLOW + "\nMasukkan nama obat yang ingin Anda beli: ").capitalize()
        try:
            jumlah_beli = int(input(Fore.YELLOW + "Masukkan jumlah yang ingin Anda beli: "))
            obat, jumlah = beli_obat_detail(obat_list, nama_obat, jumlah_beli)
            if obat:
                for i, item in enumerate(pembelian_list):
                    if item[0].nama == obat.nama:
                        pembelian_list[i] = (item[0], item[1] + jumlah)
                        break
                else:
                    pembelian_list.append((obat, jumlah))
                    os.system('cls')
            else:
                break
                
            tambah_obat_choice = input(Fore.YELLOW + "Apakah Anda ingin menambah obat lain? (y/n): ").lower()
            os.system('cls')  
            if tambah_obat_choice != 'y':
                break
        except ValueError:
            print(Fore.RED + "Mohon masukkan jumlah yang valid.")

    if pembelian_list:
        print_struk(pembelian_list)
        new_transaction_data = []
        for item in pembelian_list:
            obat, jumlah_beli = item
            new_transaction_data.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), obat.nama, jumlah_beli, obat.harga, obat.harga * jumlah_beli])

        print_struk(pembelian_list)

        add_transaksi_to_csv('transaksi.csv', new_transaction_data)


def beli_obat_detail(obat_list, nama_obat, jumlah_beli):
    merge_sort(obat_list, 'nama')

    idx = binary_search(obat_list, 'nama', nama_obat)
    if idx != -1:
        obat = obat_list[idx]
        if obat.stok > 0:
            if jumlah_beli > 0:
                if obat.stok >= jumlah_beli:
                    obat.stok -= jumlah_beli
                    obat.terjual += jumlah_beli
                    write_obat('obat.csv', obat_list)
                    return obat, jumlah_beli
                else:
                    print("Jumlah beli melebihi stok yang tersedia.")
                    return None, 0
            else:
                print("Jumlah beli tidak valid.")
                return None, 0
        else:
            print(f"Obat {obat.nama} sudah habis.")
            return None, 0
    else:
        print("Obat tidak ditemukan.")
        return None, 0


def print_struk(pembelian_list):
    os.system('cls')
    print(Fore.YELLOW + " " * 25 + "E-PHARMACY")
    print(Fore.YELLOW + " " * 22 + "STRUK PEMBELIAN")
    print(Fore.YELLOW + "Tanggal Transaksi:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  
    print(Fore.BLUE + "{:<20} | {:<10} | {:<10} | {:<10}".format("Nama Barang", "Qty", "Harga", "Sub Total")) 
    print(Fore.WHITE + "-" * 60)
    total_harga = 0
    for item in pembelian_list:
        obat, jumlah_beli = item
        subtotal = obat.harga * jumlah_beli
        total_harga += subtotal
        print(Fore.WHITE + "{:<20} | {:<10} | {:<10} | {:<10}".format(obat.nama, jumlah_beli, obat.harga, subtotal)) 
        print(Fore.WHITE + "-" * 60)
    print(Fore.WHITE + "{:<20} | {:<10} | {:<10} | {:<10}".format("TOTAL :", "", "", total_harga))
    print(Fore.YELLOW + "=" * 60)
    print(Fore.WHITE + '--- Terima Kasih Telah Berkunjung Ke Apotek Kami ---')

def cari_obat(obat_list):
    print(Fore.BLUE + "=========================================")
    print(Fore.YELLOW + "            CARI OBAT                   ")
    print(Fore.BLUE + "=========================================")
    search_option = input(Fore.CYAN + "\nPilih metode pencarian:\n1. Berdasarkan nama obat\n2. Berdasarkan kondisi kesehatan\n3. Berdasarkan kategori\nMasukkan pilihan pencarian Anda : ")
    os.system('cls') 
    
    if search_option == '1':
        cari_nama = input(Fore.YELLOW + "\nMasukkan nama obat yang ingin anda cari: ").capitalize()
        merge_sort(obat_list, 'nama')
        idx = binary_search(obat_list, 'nama', cari_nama)
        if idx != -1:
            display_obat_info(obat_list[idx]) 
        else:
            print(Fore.RED + "Obat tidak ditemukan.")

    elif search_option == '2':
        cari_kondisi = input(Fore.YELLOW + "\nMasukkan kondisi kesehatan yang ingin Anda cari: ").capitalize()
        
        merge_sort(obat_list, 'kondisi_kesehatan')

        matching_obats = []
        idx = binary_search(obat_list, 'kondisi_kesehatan', cari_kondisi)
        if idx != -1:
            matching_obats.append(obat_list[idx])
            left_idx = idx - 1
            while left_idx >= 0 and obat_list[left_idx].kondisi_kesehatan == cari_kondisi:
                matching_obats.append(obat_list[left_idx])
                left_idx -= 1
            right_idx = idx + 1
            while right_idx < len(obat_list) and obat_list[right_idx].kondisi_kesehatan == cari_kondisi:
                matching_obats.append(obat_list[right_idx])
                right_idx += 1

        if matching_obats:
            for obat in matching_obats:
                display_obat_info(obat)
        else:
            print(Fore.RED + "Obat tidak ditemukan.")
    elif search_option == '3':
        cari_kategori = input(Fore.YELLOW + "\nMasukkan kategori obat yang ingin Anda cari: ").capitalize()
        
        merge_sort(obat_list, 'kategori')

        matching_obats = []
        idx = binary_search(obat_list, 'kategori', cari_kategori)
        if idx != -1:
            matching_obats.append(obat_list[idx])
            left_idx = idx - 1
            while left_idx >= 0 and obat_list[left_idx].kategori == cari_kategori:
                matching_obats.append(obat_list[left_idx])
                left_idx -= 1
            right_idx = idx + 1
            while right_idx < len(obat_list) and obat_list[right_idx].kategori == cari_kategori:
                matching_obats.append(obat_list[right_idx])
                right_idx += 1

        if matching_obats:
            for obat in matching_obats:
                display_obat_info(obat)
    else:
        print(Fore.RED + "Pilihan tidak valid. Silakan pilih kembali.")


def user_menu(obat_list):
    filename = 'obat.csv'  
    filename_transaksi = 'transaksi.csv'
    while True:
        print(Fore.YELLOW + "=========================================")
        print(Fore.BLUE + "            MENU USER                   ")
        print(Fore.YELLOW + "=========================================")
        print(Fore.CYAN + "1. Cari Obat")
        print("2. Beli Obat")
        print("3. Kembali ke menu utama")
        user_option = input(Fore.YELLOW + "Masukkan pilihan Anda : ")

        if user_option == '1':
            time.sleep(1)
            os.system('cls')
            cari_obat(obat_list)
        elif user_option == '2':
            time.sleep(1)
            os.system('cls')
            beli_obat(obat_list)

        elif user_option == '3':
            os.system('cls')
            break



def knapsack(values, weights, budget):
    n = len(values)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, budget + 1):
            if weights[i - 1] <= j:
                dp[i][j] = max(values[i - 1] + dp[i - 1][j - weights[i - 1]], dp[i - 1][j])
            else:
                dp[i][j] = dp[i - 1][j]

    selected_drugs = []
    j = budget
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selected_drugs.append(i - 1)
            j -= weights[i - 1]

    return selected_drugs


def kelola_stok():
    file_path = 'obat.csv'
    obat_list = read_obat(file_path)
    budget = int(input(Fore.YELLOW + "Masukkan budget yang Anda miliki: "))

    values = [obat.harga for obat in obat_list]
    weights = [obat.stok for obat in obat_list]

    selected_drugs = knapsack(values, weights, budget)

    total_harga = 0
    daftar_obat = []
    for idx in selected_drugs:
        obat = obat_list[idx]
        jumlah_beli = min(obat.stok, (budget - total_harga) // obat.harga)
        if jumlah_beli > 0:
            total_harga += jumlah_beli * obat.harga
            obat.stok += jumlah_beli
            daftar_obat.append((obat.nama, jumlah_beli, obat.harga, jumlah_beli * obat.harga))

    if daftar_obat:
        print(Fore.GREEN + "Obat-obatan yang dapat dibeli dengan budget yang Anda miliki:")
        for item in daftar_obat:
            print(Fore.GREEN + f"Nama: {item[0]}, Jumlah: {item[1]}, Harga per unit: {item[2]}, Total: {item[3]}")
        print(Fore.GREEN + f"Total Harga: {total_harga}")

        write_obat(file_path, obat_list)
    else:
        print(Fore.RED + "Tidak ada obat yang bisa dibeli dengan budget tersebut.")
    input(Fore.YELLOW +"Tekan Enter untuk kembali memilih...")
    os.system('cls')


def admin_menu(obat_list):
    os.system('cls')
    while True:
        print(Fore.YELLOW + "=========================================")
        print(Fore.BLUE + "            MENU ADMIN                   ")
        print(Fore.YELLOW + "=========================================")
        print(Fore.YELLOW + "1. Tambah Admin")
        print("2. Tambah Obat")
        print("3. Hapus Obat")
        print("4. Kelola Stok")
        print("5. Tampilkan Riwayat Transaksi")
        print("6. Kembali ke menu utama")
        admin_option = input(Fore.GREEN +"Masukkan pilihan Anda (1/2/3/4/5): ")

        if admin_option == '1':
            time.sleep(1)
            os.system('cls')
            print(Fore.YELLOW + "=========================================")
            print(Fore.BLUE + "            TAMBAH ADMIN                   ")
            print(Fore.YELLOW + "=========================================")
            new_username = input(Fore.BLUE +"Masukkan username admin baru: ")
            new_password = input("Masukkan password admin baru: ")
            add_admin(new_username, new_password)
            print(Fore.GREEN + "Admin baru berhasil ditambahkan.")
            time.sleep(1)
            os.system('cls')

        elif admin_option == '2':
            time.sleep(1)
            os.system('cls')
            tambah_obat(obat_list)
            time.sleep(1)
            os.system('cls')

        elif admin_option == '3':
            time.sleep(1)
            os.system('cls')
            hapus_obat(obat_list)
            time.sleep(1)
            os.system('cls')

        elif admin_option == '4':
            time.sleep(1)
            os.system('cls')
            print(Fore.YELLOW + "=======================================================")
            print(Fore.BLUE +   "                  MENU KELOLA STOK                     ")
            print(Fore.YELLOW + "=======================================================")
            kelola_stok()
            
        elif admin_option == '5':
            time.sleep(1)
            os.system('cls')
            transaksi_list = read_transaksi('transaksi.csv')
            tampilkan_semua = input("Apakah Anda ingin menampilkan semua riwayat transaksi? (y/n): ").lower()
            if tampilkan_semua == 'y':
                display_riwayat_transaksi(transaksi_list)
            elif tampilkan_semua == 'n':
                try:
                    tanggal_transaksi = input("Masukkan tanggal transaksi yang ingin ditampilkan (yyyy-mm-dd): ")
                    display_riwayat_transaksi(transaksi_list, tanggal_transaksi)
                except ValueError:
                    print(Fore.RED + "Masukkan kode transaksi yang valid.")
            else :
                print("Input yang anda masukkan kurang tepat")
            input("Tekan Enter untuk kembali memilih...")
            os.system('cls')

        elif admin_option == '6':
            os.system('cls')
            break
        
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan pilih kembali.")
