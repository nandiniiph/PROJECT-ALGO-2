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
