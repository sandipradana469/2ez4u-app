
# stack
class Stack:

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

# postfix
def tokenisasi(ekspresi):

    tokens = []
    i = 0
    n = len(ekspresi)
    while i < n:
        c = ekspresi[i]
        if c == ' ' or c == '\t':
            i += 1
            continue
        elif c in '+-*/^()':
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
    if op == '^':
        return 3
    if op == '*' or op == '/':
        return 2
    if op == '+' or op == '-':
        return 1
    return 0

def ke_postfix(ekspresi):
    tokens = tokenisasi(ekspresi)
    stack_op = Stack()
    keluaran = []
    langkah = []
    nomor = 0

    for t in tokens:
        nomor += 1
        st = lambda: " ".join([str(x) for x in stack_op.get_items()]) or "kosong"
        out = lambda: " ".join(keluaran) or ""

        if t.isdigit():
            keluaran.append(t)
            langkah.append((f"1.{nomor}", t, "operand, langsung ke output", st(), out()))

        elif t == '(':
            stack_op.push(t)
            langkah.append((f"1.{nomor}", t, "push ( ke stack", st(), out() or "kosong"))

        elif t == ')':
            popped_kurung = []
            while not stack_op.is_empty() and stack_op.peek() != '(':
                p = stack_op.pop()
                popped_kurung.append(p)
                keluaran.append(p)
            stack_op.pop()  # buang '('
            isi_pop = " ".join(popped_kurung)
            tindakan_kurung = f"pop sampai ( : {isi_pop}, lalu buang (" if isi_pop else "pop sampai (, buang ("
            langkah.append((f"1.{nomor}", t, tindakan_kurung, st() or "kosong", out()))

        elif t in '+-*/^':
            popped = []
            while (not stack_op.is_empty() and stack_op.peek() != '(' and
                   presedensi(stack_op.peek()) >= presedensi(t)):
                p = stack_op.pop()
                popped.append(p)
                keluaran.append(p)

            stack_op.push(t)

            if popped:
                tindakan = f"pop {' '.join(popped)}, lalu push {t}"
            else:
                tindakan = f"push {t}"

            langkah.append((f"1.{nomor}", t, tindakan, st(), out()))

    sisa_op = []
    while not stack_op.is_empty():
        p = stack_op.pop()
        sisa_op.append(p)
        keluaran.append(p)

    ket_sisa = f"pop sisa stack: {' '.join(sisa_op)}" if sisa_op else "pop sisa stack"
    langkah.append(("1.akhir", "-", ket_sisa, "kosong", " ".join(keluaran)))

    return keluaran, langkah

def hitung(postfix):
    stack_val = Stack()
    langkah = []
    nomor = 0

    for t in postfix:
        nomor += 1
        if t.isdigit():
            stack_val.push(int(t))
            stack_str = " ".join([str(x) for x in stack_val.get_items()])
            langkah.append((f"2.{nomor}", t, f"operand, push {t}", stack_str))
        elif t in '+-*/^':
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
            elif t == '^':
                hasil = a ** b

            stack_val.push(hasil)
            stack_str = " ".join([str(x) for x in stack_val.get_items()])
            langkah.append((f"2.{nomor}", t, f"pop {b} dan {a} -> {a}{t}{b} = {hasil}", stack_str))

    total = stack_val.pop()
    return total, langkah

# queue naif
class QueueNaif:

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
        if self.ukuran == 0:
            return [], 0

        k_nyata = min(jumlah, self.ukuran)
        keluar = [None] * k_nyata
        for i in range(k_nyata):
            keluar[i] = self.data[i]
        total_digeser = 0
        for langkah in range(k_nyata):
            sisa_elemen = self.ukuran - (langkah + 1)
            total_digeser += sisa_elemen

        sisa = self.ukuran - k_nyata
        for i in range(sisa):
            self.data[i] = self.data[i + k_nyata]
        for i in range(sisa, self.ukuran):
            self.data[i] = None

        self.ukuran -= k_nyata
        return keluar, total_digeser

    def kembalikan_ke_depan(self, daftar_pesanan):
        k = len(daftar_pesanan)
        while self.ukuran + k > self.kapasitas:
            self._resize(2 * self.kapasitas)

        for i in range(self.ukuran - 1, -1, -1):
            self.data[i + k] = self.data[i]
        for i in range(k):
            self.data[i] = daftar_pesanan[i]
        self.ukuran += k

    def clear(self):
        for i in range(self.ukuran):
            self.data[i] = None
        self.ukuran = 0

# circular queue
class AntreanMelingkar:

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
        k = len(daftar_pesanan)
        while self.count + k > self.kapasitas:
            self._resize(2 * self.kapasitas)

        for i in range(k - 1, -1, -1):
            self.front = (self.front - 1 + self.kapasitas) % self.kapasitas
            self.data[self.front] = daftar_pesanan[i]
            self.count += 1

    def keluarkan_dari_belakang(self):
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

# undo redo
class ManajerUndoRedo:
    def __init__(self):
        self.stack_undo = Stack()
        self.stack_redo = Stack()

    def catat_aksi(self, jenis, data):
        self.stack_undo.push((jenis, data))
        self.stack_redo.clear()

    def undo(self, queue_circular, queue_naif=None):
        if self.stack_undo.is_empty():
            return "Tumpukan undo kosong, tidak ada aksi yang bisa dibatalkan."

        aksi = self.stack_undo.pop()
        jenis, data = aksi

        if jenis == 'ENQUEUE':

            dihapus = queue_circular.keluarkan_dari_belakang()
            if queue_naif and queue_naif.ukuran > 0:
                queue_naif.ukuran -= 1
                queue_naif.data[queue_naif.ukuran] = None
            pesan = f"{dihapus[0] if dihapus else 'Pesanan'} dikeluarkan lagi dari belakang antrean circular"

        elif jenis == 'DEQUEUE':

            queue_circular.kembalikan_ke_depan(data)
            if queue_naif:
                queue_naif.kembalikan_ke_depan(data)
            pesan = f"{len(data)} pesanan dikembalikan ke DEPAN kedua antrean"

        else:
            pesan = f"Aksi {jenis} dibatalkan"

        self.stack_redo.push(aksi)
        return pesan

    def redo(self, queue_circular, queue_naif=None):
        if self.stack_redo.is_empty():
            return "Tumpukan redo kosong, tidak ada yang diulang."

        aksi = self.stack_redo.pop()
        jenis, data = aksi

        if jenis == 'ENQUEUE':

            queue_circular.enqueue(data)
            if queue_naif:
                queue_naif.enqueue(data)
            pesan = f"{data[0]} masuk kembali ke belakang antrean circular"

        elif jenis == 'DEQUEUE':

            k = len(data)
            keluar, _ = queue_circular.dequeue(k)
            if queue_naif:
                queue_naif.dequeue(k)
            pesan = f"{len(keluar)} pesanan keluar lagi dari kedua antrean"

        else:
            pesan = f"Aksi {jenis} diulang"

        self.stack_undo.push(aksi)
        return pesan

    def stats(self):
        return self.stack_undo.size(), self.stack_redo.size()





