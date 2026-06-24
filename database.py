import os
import csv

# Membuat folder data jika belum ada
if not os.path.exists('data'):
    os.makedirs('data')

FILE_USER = 'data/pengguna.csv'
FILE_PRODUK = 'data/produk.csv'

def init_db():
    """Membuat file CSV dengan header default jika belum ada."""
    if not os.path.exists(FILE_USER):
        with open(FILE_USER, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_user', 'username', 'password', 'nama', 'role', 'saldo'])
            # Akun bawaan agar bisa langsung ditandai
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
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
    return users

def get_user_by_id(id_user):
    for u in get_semua_user():
        if u['id_user'] == id_user: return u
    return None

def get_user_by_username(username):
    for u in get_semua_user():
        if u['username'] == username: return u
    return None

def buat_user(username, password, nama, role, saldo):
    if get_user_by_username(username):
        raise ValueError("Username sudah terdaftar!")
    id_user = f"USR{len(get_semua_user()) + 1:03d}"
    with open(FILE_USER, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([id_user, username, password, nama, role, saldo])

def update_user(id_user, **kwargs):
    users = get_semua_user()
    for u in users:
        if u['id_user'] == id_user:
            u.update(kwargs)
    with open(FILE_USER, 'w', newline='', encoding='utf-8') as f:
        if users:
            writer = csv.writer(f)
            writer.writerow(users[0].keys())
            for u in users: writer.writerow(u.values())

def get_semua_produk():
    prods = []
    if not os.path.exists(FILE_PRODUK): return prods
    with open(FILE_PRODUK, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: prods.append(row)
    return prods

def get_produk_by_id(id_produk):
    for p in get_semua_produk():
        if p['id_produk'] == id_produk: return p
    return None

def get_produk_by_penjual(id_penjual):
    return [p for p in get_semua_produk() if p['id_penjual'] == id_penjual]

def buat_produk(id_penjual, nama_produk, kategori, harga, stok, deskripsi):
    id_produk = f"PRD{len(get_semua_produk()) + 1:03d}"
    with open(FILE_PRODUK, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([id_produk, id_penjual, nama_produk, kategori, harga, stok, deskripsi])

def update_produk(): pass
def kurangi_stok(): pass
def get_semua_pesanan(): return []
def get_pesanan_by_id(): return None
def get_pesanan_by_pembeli(): return []
def get_detail_pesanan(): return []
def buat_pesanan(): return {"id_pesanan": "ORD001"}