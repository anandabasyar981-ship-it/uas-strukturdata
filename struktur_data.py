# ==========================================
# STRUKTUR DATA UTAMA UNTUK MARKETPLACE
# ==========================================

# 1. LINKED LIST (Digunakan untuk Keranjang Belanja)
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
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self._size += 1

    def to_list(self):
        res = []
        curr = self.head
        while curr:
            res.append(curr.data)
            curr = curr.next
        return res


# 2. STACK (Digunakan untuk Riwayat/Log Aksi Pengguna)
class Stack:
    def __init__(self, max_size=30):
        self.items = []
        self.max_size = max_size

    def push(self, item):
        if len(self.items) >= self.max_size:
            self.items.pop(0) # Hapus yang paling lama jika penuh
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

    def to_list(self):
        return self.items[::-1] # Kembalikan dari yang terbaru


# 3. HASH MAP (Digunakan untuk Opsi Pencarian Cepat/Mapping Produk)
class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return sum(ord(c) for c in str(key)) % self.size

    def set(self, key, value):
        hash_key = self._hash(key)
        for pair in self.table[hash_key]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[hash_key].append([key, value])

    def get(self, key):
        hash_key = self._hash(key)
        for pair in self.table[hash_key]:
            if pair[0] == key:
                return pair[1]
        return None


# 4. BINARY SEARCH TREE / BST (Digunakan untuk Indexing/Sorting Harga)
class BSTNode:
    def __init__(self, key, value):
        self.key = key       # Ini harga (integer)
        self.value = value   # Ini data produk (dictionary)
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if not self.root:
            self.root = BSTNode(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, root, key, value):
        if key < root.key:
            if not root.left:
                root.left = BSTNode(key, value)
            else:
                self._insert(root.left, key, value)
        else:
            if not root.right:
                root.right = BSTNode(key, value)
            else:
                self._insert(root.right, key, value)


# 5. ALGORITMA SORTING & SEARCHING (Merge Sort & Binary Search)
def merge_sort(arr, key_func):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_func)
    right = merge_sort(arr[mid:], key_func)
    return _merge(left, right, key_func)

def _merge(left, right, key_func):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

def binary_search(arr, target, key_func):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = key_func(arr[mid])
        if mid_val == target:
            return arr[mid]
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return None