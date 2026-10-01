# Proyek 2EZ4U APP - Delivery Service Engine
Studi Kasus Proyek Akhir Struktur Data & Analisa Algoritma (EC234303)  
Departemen Teknik Komputer, FTEIC - ITS  
Dosen Pengampu: Ir. Arta Kusuma Hernanda, S.T., M.T.

**Data Mahasiswa:**
* Nama: Moh Luthfi Sandi Pradana
* NRP: 5024251022
* Kelas: Struktur Data & Analisa Algoritma

---

## 1. Deskripsi Proyek
Proyek 2EZ4U APP adalah aplikasi backend engine mini untuk layanan pesan antar makanan dan barang (seperti versi mini GoFood atau GrabFood) yang diuji menggunakan dataset berukuran 200.000 data.

Aplikasi ini dibangun menggunakan arsitektur 3 layer:
1. Data (data/): Berisi file `pesanan.csv` (200.000 baris) dan `peta.csv`.
2. Backend (backend/): Berisi modul struktur data dan algoritma yang diimplementasikan secara manual dari awal.
3. Frontend (frontend/): Satu jendela desktop sederhana menggunakan Tkinter untuk menjalankan perintah, melihat hasil, dan mencatat waktu eksekusi dalam milidetik (ms).

---

## 2. Struktur Repositori
```text
2ez4u-app/
|-- README.md
|-- app.py
|-- .gitignore
|-- data/
|   |-- pesanan.csv
|   `-- peta.csv
|-- backend/
|   |-- m1_pesanan.py
|   |-- m2_antrean.py
|   |-- m3_laporan.py
|   |-- m4_pencarian.py
|   |-- m5_katalog.py
|   `-- m6_peta.py
`-- frontend/
    `-- ui.py
```

---

## 3. Cara Menjalankan Aplikasi
1. Pastikan komputer sudah terpasang Python versi 3.11 atau yang lebih baru.
2. Pastikan file `pesanan.csv` dan `peta.csv` sudah berada di dalam folder `data/`.
3. Buka terminal atau PowerShell pada folder proyek ini.
4. Jalankan perintah:
```bash
python app.py
```
Aplikasi antarmuka Tkinter akan terbuka dan otomatis memuat data pesanan.

---

## 4. Implementasi dan Analisis Struktur Data

### Milestone 1 (M1): Array Dinamis vs Linked List
Pada M1, data pesanan disimpan pada dua struktur data buatan sendiri secara bersamaan agar performanya dapat diadu langsung.

Aturan bisnis posisi pesanan:
* Pesanan REGULER (prioritas 3): Mengantre di barisan paling belakang.
* Pesanan PRIORITAS (prioritas 2): Menyerobot ke tengah barisan (indeks n // 2).
* Pesanan VIP (prioritas 1): Langsung masuk ke urutan pertama (indeks 0).

Penjelasan struktur data:
1. **Array Dinamis (class Array)**
   * Dibuat menggunakan alokasi memori berukuran tetap.
   * Ketika kapasitas penuh, kapasitas digandakan 2x lipat dan elemen lama disalin manual satu per satu ke petak baru (Amortized O(1)).
   * Operasi akses data (`get`) berjalan dalam waktu konstan O(1) karena langsung melompat ke alamat indeks memori.
   * Operasi penyisipan (`insert`) dan penghapusan (`hapus`) membutuhkan waktu O(n) karena harus menggeser elemen.

2. **Singly Linked List (class LinkList)**
   * Dibuat menggunakan simpul (Node) yang saling terhubung melalui pointer next.
   * Menyimpan penunjuk `head` dan `tail`.
   * Operasi tambah REGULER berjalan dalam O(1) karena langsung ditempelkan pada pointer `tail`.
   * Operasi tambah VIP berjalan dalam O(1) karena langsung disambungkan pada pointer `head`.
   * Operasi tambah PRIORITAS berjalan dalam O(n) karena harus menelusuri simpul dari depan hingga mencapai posisi tengah.
   * Operasi akses data (`get`) berjalan dalam O(n) karena tidak ada indeks acak, sehingga harus menelusuri rantai dari `head`.

Hasil pengujian pada data 200.000 baris:
* **Lihat Pesanan**: Array unggul mutlak (~0.00 ms) dibanding Linked List (~0.07 ms pada indeks 788) karena sifat random access.
* **Tambah VIP**: Linked List unggul mutlak (~0.00 ms) dibanding Array (~6.82 ms) karena Linked List hanya memindahkan pointer `head`, sedangkan Array harus menggeser 200.000 elemen ke kanan.
* **Tambah Reguler**: Keduanya sama-sama sangat cepat (~0.00 - 0.02 ms) karena sama-sama menempel di ujung belakang.
* **Tambah Prioritas**: Keduanya membutuhkan waktu sekitar 2 - 3 ms dengan alasan berbeda: Array sibuk menggeser 100.000 elemen, sedangkan Linked List menelusuri 100.000 simpul.

---

### Milestone 2 (M2): Stack, Queue, Mesin Kasir Postfix, dan Fitur Undo/Redo

1. **Mesin Kasir Postfix (class Stack)**
   * Mengubah ekspresi struk belanja dari bentuk infix ke postfix menggunakan Stack operator berdasarkan prioritas (* dan / lebih tinggi dari + dan -).
   * Mengevaluasi postfix menggunakan Stack nilai.
   * Urutan pop diperhatikan secara ketat: operand kanan diambil terlebih dahulu (`b = pop()` lalu `a = pop()`), kemudian dihitung `a - b` atau `a // b` agar operasi pengurangan dan pembagian tidak terbalik.
   * Menampilkan tabel langkah demi langkah konversi dan evaluasi.

2. **Perbandingan Dua Versi Queue**
   * **Queue Naif (class QueueNaif)**: Berbasis array biasa. Saat melayani pesanan (dequeue), elemen pertama diambil dan seluruh sisa elemen digeser ke kiri. Kompleksitasnya O(n) per layanan. Pada pengujian 100 pesanan dari 14.376 antrean, terjadi pergeseran lebih dari 1,4 juta elemen fisik di memori.
   * **Antrean Melingkar (class AntreanMelingkar)**: Berbasis circular array menggunakan penunjuk `front`, `rear`, dan variabel `count`. Dequeue hanya memajukan penunjuk `front` menggunakan operasi modulo `(front + 1) % kapasitas`. Kompleksitasnya O(1) dan 0 elemen yang digeser di memori.

3. **Fitur Undo dan Redo (class ManajerUndoRedo)**
   * Menggunakan dua buah stack (stack undo dan stack redo).
   * Setiap ada aksi baru (enqueue / dequeue), aksi dicatat ke stack undo dan stack redo otomatis dikosongkan.
   * Fungsi `undo` membatalkan efek aksi terakhir: jika aksi sebelumnya dequeue, seluruh pesanan yang keluar dikembalikan ke DEPAN antrean circular.
   * Fungsi `redo` mengerjakan kembali aksi yang baru saja dibatalkan.

---

## 5. Kepatuhan Aturan Main
Seluruh kode backend dibuat dengan mematuhi batasan tugas dari dosen:
* Tidak menggunakan tipe data dan struktur bawaan: `dict`, `set`, dan literal `{}`.
* Tidak menggunakan fungsi sorting bawaan: `sorted()` atau `.sort()`.
* Tidak menggunakan pustaka bawaan: `collections.*`, `heapq`, dan `bisect`.
* List Python hanya digunakan sebagai array primitif berukuran tetap.
* Operasi yang digunakan adalah tuple, manipulasi pointer simpul, aritmetika, dan file I/O standar.
