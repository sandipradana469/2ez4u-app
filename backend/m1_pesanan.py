# --- LOGIKA ARRAY DINAMIS ---
class Array:
    def __init__(self, kapasitas_awal=4):
        self.kapasitas = kapasitas_awal
        self.ukuran = 0
        self.data = [None] * self.kapasitas
        
    def _resize(self, kapasitas_baru):
        data_baru = [None] * kapasitas_baru
        for i in range(self.ukuran):
            data_baru[i] = self.data[i]
        self.data = data_baru
        self.kapasitas = kapasitas_baru

    def append(self, v):
        # Tambah REGULER (di belakang) - Amortized O(1)
        if self.ukuran == self.kapasitas:
            self._resize(2 * self.kapasitas)
        self.data[self.ukuran] = v
        self.ukuran += 1

    def insert(self, indeks, v):
        # Tambah PRIORITAS/VIP - O(n) karena harus geser elemen
        if self.ukuran == self.kapasitas:
            self._resize(2 * self.kapasitas)
        for i in range(self.ukuran, indeks, -1):
            self.data[i] = self.data[i - 1]
        self.data[indeks] = v
        self.ukuran += 1

    def get(self, indeks):
        if 0 <= indeks < self.ukuran:
            return self.data[indeks]
        return None
        
    def hapus(self, indeks):
        if 0 <= indeks < self.ukuran:
            for i in range(indeks, self.ukuran - 1):
                self.data[i] = self.data[i + 1]
            self.data[self.ukuran - 1] = None
            self.ukuran -= 1


# --- LOGIKA LINKED LIST ---
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.ukuran = 0

    def append(self, v):
        # Tambah REGULER (di belakang) - O(1) karena ada tail
        simpul_baru = Node(v)
        if not self.head:
            self.head = self.tail = simpul_baru
        else:
            self.tail.next = simpul_baru
            self.tail = simpul_baru
        self.ukuran += 1

    def insert(self, indeks, v):
        # Tambah PRIORITAS (tengah) atau VIP (depan)
        if indeks <= 0: # VIP masuk paling depan - O(1)
            simpul_baru = Node(v)
            simpul_baru.next = self.head
            self.head = simpul_baru
            if self.ukuran == 0:
                self.tail = simpul_baru
            self.ukuran += 1
            return
            
        if indeks >= self.ukuran:
            self.append(v)
            return
            
        # PRIORITAS masuk tengah - O(n) telusur
        simpul_baru = Node(v)
        sekarang = self.head
        for _ in range(indeks - 1):
            sekarang = sekarang.next
            
        simpul_baru.next = sekarang.next
        sekarang.next = simpul_baru
        self.ukuran += 1

    def get(self, indeks):
        if indeks < 0 or indeks >= self.ukuran:
            return None
        sekarang = self.head
        for _ in range(indeks):
            sekarang = sekarang.next
        return sekarang.data

    def hapus(self, indeks):
        if indeks < 0 or indeks >= self.ukuran:
            return None
        
        if indeks == 0:
            dihapus = self.head
            self.head = self.head.next
            if self.ukuran == 1:
                self.tail = None
            self.ukuran -= 1
            return dihapus.data
            
        sekarang = self.head
        for _ in range(indeks - 1):
            sekarang = sekarang.next
            
        dihapus = sekarang.next
        sekarang.next = dihapus.next
        if dihapus == self.tail:
            self.tail = sekarang
            
        self.ukuran -= 1
        return dihapus.data