#M2 antrean

class Stack:
    #Implementasi tumpukan (LIFO) menggunakan array primitif dinamis.
    def __init__(self, kapasitas_awal=16):
        self.kapasitas = kapasitas_awal
        self.top = 0
        self.data = [None] * self.kapasitas

    def _resize(self, kapasitas_baru):
        data_baru = [None] * kapasitas_baru
        for i in range(self.top):
            data_baru[i] = self.data[i]
        self.data = data_baru
        self.kapasitas = kapasitas_baru

    def push(self, x):
        if self.top == self.kapasitas:
            self._resize(2 * self.kapasitas)
        self.data[self.top] = x
        self.top += 1

    def pop(self):
        if self.top == 0:
            return None
        self.top -= 1
        nilai = self.data[self.top]
        self.data[self.top] = None
        return nilai

    def peek(self):
        if self.top == 0:
            return None
        return self.data[self.top - 1]

    def is_empty(self):
        return self.top == 0

    def size(self):
        return self.top

    def get_items(self):
        hasil = [None] * self.top
        for i in range(self.top):
            hasil[i] = self.data[i]
        return hasil

    def clear(self):
        for i in range(self.top):
            self.data[i] = None
        self.top = 0

# BAGIAN A (1): KASIR (INFIX -> POSTFIX -> EVALUASI)
def tokenisasi(ekspresi):
    """Memecah string ekspresi menjadi list token (angka, operator, kurung)."""
    tokens = []
    i = 0
    n = len(ekspresi)
    while i < n:
        c = ekspresi[i]
        if c == ' ' or c == '\t':
            i += 1
            continue
        elif c in '+-*/()':
            tokens.append(c)
            i += 1
        elif c.isdigit():
            j = i
            while j < n and ekspresi[j].isdigit():
                j += 1
            tokens.append(ekspresi[i:j])
            i = j
        else:
            i += 1
    return tokens

def presedensi(op):
    if op == '*' or op == '/':
        return 2
    if op == '+' or op == '-':
        return 1
    return 0

def ke_postfix(ekspresi):
    """
    Mengubah infix ke postfix memakai Stack operator.
    Mengembalikan (list_postfix, langkah_tabel).
    """
    tokens = tokenisasi(ekspresi)
    stack_op = Stack()
    keluaran = []
    langkah = []

    for t in tokens:
        if t.isdigit():
            keluaran.append(t)
            stack_str = " ".join([str(x) for x in stack_op.get_items()])
            out_str = " ".join(keluaran)
            langkah.append((t, "angka, langsung keluar", stack_str, out_str))
        elif t == '(':
            stack_op.push(t)
            stack_str = " ".join([str(x) for x in stack_op.get_items()])
            out_str = " ".join(keluaran)
            langkah.append((t, "push (", stack_str, out_str))
        elif t == ')':
            while not stack_op.is_empty() and stack_op.peek() != '(':
                keluaran.append(stack_op.pop())
            stack_op.pop() # Buang tanda '('
            stack_str = " ".join([str(x) for x in stack_op.get_items()]) if not stack_op.is_empty() else "kosong"
            out_str = " ".join(keluaran)
            langkah.append((t, "pop sampai (, buang (", stack_str, out_str))
        elif t in '+-*/':
            while (not stack_op.is_empty() and stack_op.peek() != '(' and
                   presedensi(stack_op.peek()) >= presedensi(t)):
                keluaran.append(stack_op.pop())
            stack_op.push(t)
            stack_str = " ".join([str(x) for x in stack_op.get_items()])
            out_str = " ".join(keluaran)
            langkah.append((t, f"push {t}", stack_str, out_str))

    while not stack_op.is_empty():
        keluaran.append(stack_op.pop())
    
    out_str = " ".join(keluaran)
    langkah.append(("akhir", "pop sisa stack", "kosong", out_str))

    return keluaran, langkah

def hitung(postfix):
    """
    Mengevaluasi ekspresi postfix memakai Stack nilai.
    Mengembalikan (total_nilai, langkah_tabel).
    Perhatian: Urutan pop b = pop() dulu, baru a = pop(), hitung a op b.
    """
    stack_val = Stack()
    langkah = []

    for t in postfix:
        if t.isdigit():
            stack_val.push(int(t))
            stack_str = " ".join([str(x) for x in stack_val.get_items()])
            langkah.append((t, f"push {t}", stack_str))
        elif t in '+-*/':
            b = stack_val.pop()
            a = stack_val.pop()
            if a is None or b is None:
                continue

            if t == '+':
                hasil = a + b
            elif t == '-':
                hasil = a - b
            elif t == '*':
                hasil = a * b
            elif t == '/':
                hasil = a // b if b != 0 else 0

            stack_val.push(hasil)
            stack_str = " ".join([str(x) for x in stack_val.get_items()])
            langkah.append((t, f"pop {b} dan {a} -> {a}{t}{b} = {hasil}", stack_str))

    total = stack_val.pop()
    return total, langkah

# BAGIAN B: DUA VERSI QUEUE (NAIF VS MELINGKAR)
class QueueNaif:
    """Antrean berbasis array biasa. Dequeue memerlukan penggeseran elemen O(n)."""
    def __init__(self, kapasitas_awal=32):
        self.kapasitas = kapasitas_awal
        self.ukuran = 0
        self.data = [None] * self.kapasitas

    def _resize(self, kapasitas_baru):
        data_baru = [None] * kapasitas_baru
        for i in range(self.ukuran):
            data_baru[i] = self.data[i]
        self.data = data_baru
        self.kapasitas = kapasitas_baru

    def enqueue(self, x):
        if self.ukuran == self.kapasitas:
            self._resize(2 * self.kapasitas)
        self.data[self.ukuran] = x
        self.ukuran += 1

    def dequeue(self, jumlah=1):
        """
        Melayani 'jumlah' pesanan dari depan antrean.
        Mengembalikan tuple (list_pesanan_keluar, total_elemen_digeser).
        """
        if self.ukuran == 0:
            return [], 0

        k_nyata = min(jumlah, self.ukuran)
        keluar = [None] * k_nyata
        for i in range(k_nyata):
            keluar[i] = self.data[i]

        # Hitung total elemen yang digeser:
        # Jika k pesanan keluar bertahap, tiap langkah menggeser sisa elemen
        total_digeser = 0
        for langkah in range(k_nyata):
            sisa_elemen = self.ukuran - (langkah + 1)
            total_digeser += sisa_elemen

        # Geser fisik elemen ke depan
        sisa = self.ukuran - k_nyata
        for i in range(sisa):
            self.data[i] = self.data[i + k_nyata]
        for i in range(sisa, self.ukuran):
            self.data[i] = None

        self.ukuran -= k_nyata
        return keluar, total_digeser

    def clear(self):
        for i in range(self.ukuran):
            self.data[i] = None
        self.ukuran = 0


class AntreanMelingkar:
    
    #Antrean melingkar (Circular Queue) berbasis array dengan penunjuk front, rear, dan count.
    #Operasi enqueue O(1) dan dequeue O(1) tanpa penggeseran elemen memori.

    def __init__(self, kapasitas_awal=32768):
        self.kapasitas = kapasitas_awal
        self.data = [None] * self.kapasitas
        self.front = 0
        self.rear = 0
        self.count = 0

    def _resize(self, kapasitas_baru):
        data_baru = [None] * kapasitas_baru
        for i in range(self.count):
            data_baru[i] = self.data[(self.front + i) % self.kapasitas]
        self.data = data_baru
        self.front = 0
        self.rear = self.count
        self.kapasitas = kapasitas_baru

    def enqueue(self, x):
        if self.count == self.kapasitas:
            self._resize(2 * self.kapasitas)
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.kapasitas
        self.count += 1

    def dequeue(self, jumlah=1):
        """
        Melayani 'jumlah' pesanan dari depan antrean secara O(1).
        Mengembalikan tuple (list_pesanan_keluar, 0) karena 0 elemen digeser.
        """
        if self.count == 0:
            return [], 0

        k_nyata = min(jumlah, self.count)
        keluar = [None] * k_nyata
        for i in range(k_nyata):
            keluar[i] = self.data[self.front]
            self.data[self.front] = None
            self.front = (self.front + 1) % self.kapasitas
            self.count -= 1

        return keluar, 0

    def kembalikan_ke_depan(self, daftar_pesanan):
        """
        Mengembalikan seluruh pesanan ke DEPAN antrean (dipakai untuk UNDO aksi dequeue).
        """
        k = len(daftar_pesanan)
        while self.count + k > self.kapasitas:
            self._resize(2 * self.kapasitas)

        # Kembalikan dengan urutan terbalik agar elemen pertama kembali menjadi front
        for i in range(k - 1, -1, -1):
            self.front = (self.front - 1 + self.kapasitas) % self.kapasitas
            self.data[self.front] = daftar_pesanan[i]
            self.count += 1

    def keluarkan_dari_belakang(self):
        """
        Mencabut 1 pesanan dari belakang antrean (dipakai untuk UNDO aksi enqueue).
        """
        if self.count == 0:
            return None
        self.rear = (self.rear - 1 + self.kapasitas) % self.kapasitas
        dihapus = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return dihapus

    def is_empty(self):
        return self.count == 0

    def size(self):
        return self.count

    def clear(self):
        self.front = 0
        self.rear = 0
        self.count = 0
        self.data = [None] * self.kapasitas

# BAGIAN A (2): STACK UNDO & REDO
class ManajerUndoRedo:
    """
    Mengelola tumpukan undo dan redo.
    Aturan: Aksi baru apa pun mengosongkan tumpukan redo.
    """
    def __init__(self):
        self.stack_undo = Stack()
        self.stack_redo = Stack()

    def catat_aksi(self, jenis, data):
        """
        Mencatat aksi baru ke stack undo dan MENGOSONGKAN stack redo.
        jenis: 'ENQUEUE' atau 'DEQUEUE'
        """
        self.stack_undo.push((jenis, data))
        self.stack_redo.clear()

    def undo(self, queue_circular, queue_naif=None):
        """
        Membatalkan aksi terakhir dari stack undo.
        Mengembalikan pesan status.
        """
        if self.stack_undo.is_empty():
            return "Tumpukan undo kosong, tidak ada aksi yang bisa dibatalkan."

        aksi = self.stack_undo.pop()
        jenis, data = aksi

        if jenis == 'ENQUEUE':
            # Kebalikan enqueue: keluarkan lagi pesanan dari belakang antrean
            dihapus = queue_circular.keluarkan_dari_belakang()
            if queue_naif and queue_naif.ukuran > 0:
                queue_naif.ukuran -= 1
                queue_naif.data[queue_naif.ukuran] = None
            pesan = f"{dihapus[0] if dihapus else 'Pesanan'} dikeluarkan lagi dari belakang antrean circular"

        elif jenis == 'DEQUEUE':
            # Kebalikan dequeue: kembalikan seluruh pesanan ke DEPAN antrean circular
            queue_circular.kembalikan_ke_depan(data)
            pesan = f"{len(data)} pesanan dikembalikan ke DEPAN antrean circular"

        else:
            pesan = f"Aksi {jenis} dibatalkan"

        # Simpan aksi yang dibatalkan ke stack redo
        self.stack_redo.push(aksi)
        return pesan

    def redo(self, queue_circular, queue_naif=None):
        """
        Mengerjakan kembali aksi yang baru saja dibatalkan oleh undo.
        Mengembalikan pesan status.
        """
        if self.stack_redo.is_empty():
            return "Tumpukan redo kosong, tidak ada yang diulang."

        aksi = self.stack_redo.pop()
        jenis, data = aksi

        if jenis == 'ENQUEUE':
            # Kerjakan lagi enqueue aslinya
            queue_circular.enqueue(data)
            if queue_naif:
                queue_naif.enqueue(data)
            pesan = f"{data[0]} masuk kembali ke belakang antrean circular"

        elif jenis == 'DEQUEUE':
            # Kerjakan lagi dequeue aslinya
            k = len(data)
            keluar, _ = queue_circular.dequeue(k)
            pesan = f"{len(keluar)} pesanan keluar lagi dari antrean circular"

        else:
            pesan = f"Aksi {jenis} diulang"

        # Push kembali ke stack undo
        self.stack_undo.push(aksi)
        return pesan

    def stats(self):
        return self.stack_undo.size(), self.stack_redo.size()
