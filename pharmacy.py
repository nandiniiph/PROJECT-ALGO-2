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

