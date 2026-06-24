#!/usr/bin/env python3
import os, sys, time, csv

# ── 1. STRUKTUR DATA UTAMA ───────────────────────────────────────────
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0
    def __len__(self):
        return self._size
    def append(self, data):
        new_node = Node(data)
        if not self.head: self.head = new_node
        else:
            curr = self.head
            while curr.next: curr = curr.next
            curr.next = new_node
        self._size += 1
    def to_list(self):
        res = []; curr = self.head
        while curr:
            res.append(curr.data); curr = curr.next
        return res

class Stack:
    def __init__(self, max_size=30):
        self.items = []
        self.max_size = max_size
    def push(self, item):
        if len(self.items) >= self.max_size: self.items.pop(0)
        self.items.append(item)
    def to_list(self): return self.items[::-1]

class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)]
    def _hash(self, key): return sum(ord(c) for c in str(key)) % self.size
    def set(self, key, value):
        hk = self._hash(key)
        for pair in self.table[hk]:
            if pair[0] == key: pair[1] = value; return
        self.table[hk].append([key, value])
    def get(self, key):
        hk = self._hash(key)
        for pair in self.table[hk]:
            if pair[0] == key: return pair[1]
        return None

class BSTNode:
    def __init__(self, key, value):
        self.key = key; self.value = value; self.left = self.right = None

class BST:
    def __init__(self): self.root = None
    def insert(self, key, value):
        if not self.root: self.root = BSTNode(key, value)
        else: self._insert(self.root, key, value)
    def _insert(self, root, key, value):
        if key < root.key:
            if not root.left: root.left = BSTNode(key, value)
            else: self._insert(root.left, key, value)
        else:
            if not root.right: root.right = BSTNode(key, value)
            else: self._insert(root.right, key, value)

# ── 2. LOGIKA DATABASE CSV ───────────────────────────────────────────
if not os.path.exists('data'): os.makedirs('data')
FILE_USER = 'data/pengguna.csv'
FILE_PRODUK = 'data/produk.csv'

def init_db():
    if not os.path.exists(FILE_USER):
        with open(FILE_USER, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_user', 'username', 'password', 'nama', 'role', 'saldo'])
            writer.writerow(['USR001', 'penjual1', '123', 'Toko Berkah', 'penjual', '0'])
            writer.writerow(['USR002', 'pembeli1', '123', 'Budi Pembeli', 'pembeli', '1000000'])
    if not os.path.exists(FILE_PRODUK):
        with open(FILE_PRODUK, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_produk', 'id_penjual', 'nama_produk', 'kategori', 'harga', 'stok', 'deskripsi'])

def get_semua_user():
    users = []
    if not os.path.exists(FILE_USER): return users
    with open(FILE_USER, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f): users.append(row)
    return users

def get_user_by_username(username):
    for u in get_semua_user():
        if u['username'] == username: return u
    return None

def buat_user(username, password, nama, role, saldo):
    if get_user_by_username(username): raise ValueError("Username sudah ada!")
    id_user = f"USR{len(get_semua_user()) + 1:03d}"
    with open(FILE_USER, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([id_user, username, password, nama, role, saldo])

def get_semua_produk():
    prods = []
    if not os.path.exists(FILE_PRODUK): return prods
    with open(FILE_PRODUK, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f): prods.append(row)
    return prods

def buat_produk(id_penjual, nama, kategori, harga, stok, deskripsi):
    id_produk = f"PRD{len(get_semua_produk()) + 1:03d}"
    with open(FILE_PRODUK, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([id_produk, id_penjual, nama, kategori, harga, stok, deskripsi])

def proses_transaksi_csv(id_produk, qty, id_penjual, total_harga):
    """Memotong stok produk dan menambah saldo penjual secara langsung di CSV"""
    # 1. Update Stok Produk
    prods = get_semua_produk()
    for p in prods:
        if p['id_produk'] == id_produk:
            p['stok'] = str(max(0, int(p['stok']) - int(qty)))
    with open(FILE_PRODUK, 'w', newline='', encoding='utf-8') as f:
        if prods:
            writer = csv.writer(f)
            writer.writerow(prods[0].keys())
            for p in prods: writer.writerow(p.values())

    # 2. Update Saldo Penjual
    users = get_semua_user()
    for u in users:
        if u['id_user'] == id_penjual:
            u['saldo'] = str(int(u['saldo']) + int(total_harga))
    with open(FILE_USER, 'w', newline='', encoding='utf-8') as f:
        if users:
            writer = csv.writer(f)
            writer.writerow(users[0].keys())
            for u in users: writer.writerow(u.values())

# ── 3. TAMPILAN DAN ANTARMUKA CLI ────────────────────────────────────
R="\033[91m"; G="\033[92m"; Y="\033[93m"; C="\033[96m"; BLD="\033[1m"; RST="\033[0m"
def bersih(): os.system("cls" if os.name=="nt" else "clear")
def enter(): input(f"\n{Y}  [Enter] untuk lanjut...{RST}")
def rp(n): return f"Rp {int(n):,}".replace(",",".")

sesi_user = None
keranjang_ll = LinkedList()
aksi_stack = Stack()
produk_map = HashMap()

def sync_produk():
    global produk_map
    produk_map = HashMap()
    for p in get_semua_produk(): produk_map.set(p["id_produk"], p)

# ── 4. ROUTER UTAMA ──────────────────────────────────────────────────
def menu_utama():
    global sesi_user
    while True:
        if not sesi_user:
            bersih()
            print(f"{BLD}{C}══ MARKETPLACE ══{RST}")
            print("  1. Login")
            print("  2. Daftar Akun")
            print("  0. Keluar\n")
            p = input("  Pilih: ").strip()
            if p == "1": _login()
            elif p == "2": _daftar()
            elif p == "0": sys.exit()
        else:
            # Mengambil data user paling update dari database CSV setiap loop menu
            all_u = get_semua_user()
            for u in all_u:
                if u['id_user'] == sesi_user['id_user']: sesi_user = u; break
                
            if sesi_user["role"] == "penjual": menu_penjual()
            elif sesi_user["role"] == "pembeli": menu_pembeli()

def _login():
    global sesi_user
    bersih()
    print(f"{BLD}{C}══ LOGIN PENGGUNA ══{RST}")
    uname = input("  Username : ").strip()
    pwd   = input("  Password : ").strip()
    u = get_user_by_username(uname)
    if u and u["password"] == pwd:
        sesi_user = u
        print(f"\n{G}  ✔ Login sukses, Halo {u['nama']}!{RST}")
        time.sleep(1)
    else:
        print(f"\n{R}  ✘ Gagal Login!{RST}"); time.sleep(1)

def _daftar():
    bersih()
    print(f"{BLD}{C}══ DAFTAR AKUN ══{RST}")
    un = input("  Username: ").strip()
    pw = input("  Password: ").strip()
    nm = input("  Nama    : ").strip()
    rl = input("  Role (1. Pembeli | 2. Penjual): ").strip()
    role = "penjual" if rl == "2" else "pembeli"
    saldo = 0 if role == "penjual" else 1000000
    try:
        buat_user(un, pw, nm, role, saldo)
        print(f"\n{G}  ✔ Akun Berhasil Terdaftar!{RST}")
    except Exception as e: print(f"\n{R}  ✘ Gagal: {e}{RST}")
    enter()

# ── 5. HALAMAN SELLER & BUYER ────────────────────────────────────────
def menu_penjual():
    global sesi_user
    while sesi_user:
        bersih()
        print(f"{BLD}{G}══ MENU PENJUAL ({sesi_user['nama'].upper()}) ══{RST}")
        print(f"   Saldo Toko Anda: {rp(sesi_user['saldo'])}") # <─── Tampilkan Saldo Penjual Real-time
        print("  ────────────────────────────────────────")
        print("  1. Lihat Produk Toko Saya")
        print("  2. Tambah Produk Baru")
        print("  0. Logout\n")
        p = input("  Pilih: ").strip()
        if p == "1":
            bersih()
            print(f"{BLD}── PRODUK SAYA ──{RST}")
            prods = [x for x in get_semua_produk() if x['id_penjual'] == sesi_user['id_user']]
            if not prods: print("  Kosong.")
            else:
                for pr in prods: print(f"  • [{pr['id_produk']}] {pr['nama_produk']} | Harga: {rp(pr['harga'])} | Stok: {pr['stok']}")
            enter()
        elif p == "2":
            bersih()
            print(f"{BLD}── TAMBAH PRODUK BARU ──{RST}")
            nm = input("  Nama Barang: ").strip()
            kt = input("  Kategori   : ").strip()
            hg = input("  Harga (Rp) : ").strip()
            st = input("  Stok Awal  : ").strip()
            ds = input("  Deskripsi  : ").strip()
            buat_produk(sesi_user['id_user'], nm, kt, hg, st, ds)
            sync_produk()
            print(f"\n{G}  ✔ Sukses Masuk CSV!{RST}"); enter()
        elif p == "0": sesi_user = None

def menu_pembeli():
    global sesi_user
    while sesi_user:
        bersih()
        print(f"{BLD}{Y}══ MENU PEMBELI ({sesi_user['nama'].upper()}) ══{RST}")
        print("  1. Katalog Semua Produk")
        print("  2. Tambah Barang ke Keranjang")
        print("  3. Proses Checkout & Bayar")
        print("  0. Logout\n")
        p = input("  Pilih: ").strip()
        if p == "1":
            bersih()
            print(f"{BLD}── KATALOG MARKETPLACE ──{RST}")
            for pr in get_semua_produk():
                print(f"  • [{pr['id_produk']}] {pr['nama_produk']} | Harga: {rp(pr['harga'])} | Stok: {pr['stok']}")
            enter()
        elif p == "2":
            bersih()
            print(f"{BLD}── TAMBAH KE KERANJANG (LINKED LIST) ──{RST}")
            pid = input("  Masukkan ID Produk (contoh: PRD001): ").strip()
            qty = input("  Jumlah Beli: ").strip()
            p_data = produk_map.get(pid)
            if p_data and int(p_data['stok']) >= int(qty):
                keranjang_ll.append({"id_produk": pid, "nama": p_data['nama_produk'], "qty": qty})
                print(f"\n{G}  ✔ Dimasukkan ke Linked List Keranjang!{RST}")
            else: print(f"\n{R}  ✘ Produk tidak ditemukan / stok kurang!{RST}")
            enter()
        elif p == "3":
            fitur_checkout()
        elif p == "0": sesi_user = None

# ── 6. FITUR CHECKOUT & SINKRONISASI SALDO ───────────────────────────
def fitur_checkout():
    global keranjang_ll
    bersih()
    print(f"{BLD}{C}══ PROSES CHECKOUT BELANJA ══{RST}")
    
    items = keranjang_ll.to_list()
    if not items:
        print(f"{R}  ✘ Keranjang Anda kosong! Silakan isi barang dulu di menu 2.{RST}")
        enter(); return
        
    print(f"{G}  [>] Memproses transaksi belanja...{RST}")
    for it in items:
        p_data = produk_map.get(it['id_produk'])
        if p_data:
            qty_beli = int(it['qty'])
            total_harga_item = int(p_data['harga']) * qty_beli
            id_penjual = p_data['id_penjual']
            
            print(f"      - ID Produk: {it['id_produk']} | Qty: {qty_beli} | Total: {rp(total_harga_item)}")
            # Proses pemotongan stok sekaligus tambah uang ke saldo penjual di file CSV
            proses_transaksi_csv(it['id_produk'], qty_beli, id_penjual, total_harga_item)
        
    # Kosongkan Linked List Keranjang belanja setelah sukses checkout
    keranjang_ll = LinkedList()
    sync_produk() # Sinkronisasi data RAM kembali
    
    print(f"\n{G}  ✔ Transaksi Selesai!{RST}")
    print(f"{G}  ✔ Stok berkurang, keranjang dikosongkan, dan SALDO PENJUAL bertambah!{RST}")
    aksi_stack.push("Checkout Sukses")
    enter()

if __name__ == "__main__":
    init_db()
    sync_produk()
    menu_utama()