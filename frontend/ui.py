import tkinter as tk
from tkinter import messagebox
import time

from backend.m2_antrean import (
    QueueNaif,
    AntreanMelingkar,
    ManajerUndoRedo,
    ke_postfix,
    hitung
)
from backend.m3_laporan import (
    normalisasi_kunci,
    salin_data,
    insertion_sort as m3_insertion_sort,
    merge_sort as m3_merge_sort,
    linear_search as m3_linear_search,
    binary_search as m3_binary_search
)

class AppUI:
    def __init__(self, root, backend_array, backend_ll, queue_naif=None, queue_circular=None, manajer_undo=None):
        self.root = root
        self.backend_array = backend_array
        self.backend_ll = backend_ll
        self.queue_naif = queue_naif if queue_naif is not None else QueueNaif()
        self.queue_circular = queue_circular if queue_circular is not None else AntreanMelingkar()
        self.manajer_undo = manajer_undo if manajer_undo is not None else ManajerUndoRedo()

        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1100x680")

        # ================================================================
        # KONFIGURASI MENU DAN PARAMETER FORM (M1 s.d. M3)
        # ================================================================
        self.menu_config = {
            # --- DATA ---
            'DATA_LOAD': {
                'judul': 'Data: Muat Pesanan dari CSV',
                'subjudul': 'Membaca data/pesanan.csv ke dalam struktur data Array dan Linked List.',
                'field': 'File sumber data',
                'default': 'data/pesanan.csv',
                'btn': 'LOAD',
                'hint': 'klik untuk memuat atau memuat ulang dataset pesanan 200.000 baris',
                'cmd': 'load',
                'modul': 'M1 - larik',
                'aksi': 'DATA_LOAD'
            },

            # --- M1: DATA PESANAN ---
            'ARRAY_LIHAT': {
                'judul': 'Array: lihat pesanan ke-i',
                'subjudul': 'get: buka detail satu pesanan pada indeks tertentu, O(1).',
                'field': 'Indeks pesanan',
                'default': '0',
                'btn': 'LIHAT',
                'hint': 'masukkan indeks pesanan (0 s.d. n-1)',
                'cmd': 'array_get',
                'modul': 'M1 - array',
                'struktur': 'ARRAY',
                'aksi': 'LIHAT'
            },
            'ARRAY_TAMBAH_REGULER': {
                'judul': 'Array: pesanan REGULER, masuk paling belakang',
                'subjudul': 'append: pesanan biasa mengantre di barisan paling belakang.',
                'field': 'Nama pelanggan',
                'default': 'Pelanggan Baru',
                'btn': 'TAMBAH',
                'hint': 'nama untuk pesanan yang akan dibuat',
                'cmd': 'array_append',
                'modul': 'M1 - array',
                'struktur': 'ARRAY',
                'aksi': 'TAMBAH',
                'prioritas': 'REGULER'
            },
            'ARRAY_TAMBAH_PRIORITAS': {
                'judul': 'Array: pesanan PRIORITAS, masuk tengah barisan',
                'subjudul': 'insert: pesanan prioritas menyerobot ke tengah antrean (indeks n//2), O(n).',
                'field': 'Nama pelanggan',
                'default': 'Pelanggan Prioritas',
                'btn': 'TAMBAH',
                'hint': 'nama untuk pesanan yang akan dibuat',
                'cmd': 'array_insert',
                'modul': 'M1 - array',
                'struktur': 'ARRAY',
                'aksi': 'TAMBAH',
                'prioritas': 'PRIORITAS'
            },
            'ARRAY_TAMBAH_VIP': {
                'judul': 'Array: pesanan VIP, masuk paling depan',
                'subjudul': 'insert: pesanan VIP langsung ke urutan pertama (indeks 0), O(n).',
                'field': 'Nama pelanggan',
                'default': 'Pelanggan VIP',
                'btn': 'TAMBAH',
                'hint': 'nama untuk pesanan yang akan dibuat',
                'cmd': 'array_vip',
                'modul': 'M1 - array',
                'struktur': 'ARRAY',
                'aksi': 'TAMBAH',
                'prioritas': 'VIP'
            },
            'ARRAY_HAPUS': {
                'judul': 'Array: hapus pesanan ke-i',
                'subjudul': 'hapus: pesanan dicabut dari barisan pada indeks tertentu, O(n).',
                'field': 'Indeks pesanan',
                'default': '0',
                'btn': 'HAPUS',
                'hint': 'indeks pesanan yang akan dicabut dari antrean',
                'cmd': 'array_delete',
                'modul': 'M1 - array',
                'struktur': 'ARRAY',
                'aksi': 'HAPUS'
            },
            'LINKLIST_LIHAT': {
                'judul': 'Linked List: lihat pesanan ke-i',
                'subjudul': 'get: buka detail satu pesanan pada indeks tertentu, O(n) telusur.',
                'field': 'Indeks pesanan',
                'default': '0',
                'btn': 'LIHAT',
                'hint': 'masukkan indeks pesanan (0 s.d. n-1)',
                'cmd': 'll_get',
                'modul': 'M1 - rantai',
                'struktur': 'LINKLIST',
                'aksi': 'LIHAT'
            },
            'LINKLIST_TAMBAH_REGULER': {
                'judul': 'Linked List: pesanan REGULER, masuk paling belakang',
                'subjudul': 'append: pesanan biasa mengantre di barisan paling belakang, O(1) via tail.',
                'field': 'Nama pelanggan',
                'default': 'Pelanggan Baru',
                'btn': 'TAMBAH',
                'hint': 'nama untuk pesanan yang akan dibuat',
                'cmd': 'll_append',
                'modul': 'M1 - rantai',
                'struktur': 'LINKLIST',
                'aksi': 'TAMBAH',
                'prioritas': 'REGULER'
            },
            'LINKLIST_TAMBAH_PRIORITAS': {
                'judul': 'Linked List: pesanan PRIORITAS, masuk tengah barisan',
                'subjudul': 'insert: pesanan prioritas menyerobot ke tengah antrean, O(n) telusur.',
                'field': 'Nama pelanggan',
                'default': 'Pelanggan Prioritas',
                'btn': 'TAMBAH',
                'hint': 'nama untuk pesanan yang akan dibuat',
                'cmd': 'll_insert',
                'modul': 'M1 - rantai',
                'struktur': 'LINKLIST',
                'aksi': 'TAMBAH',
                'prioritas': 'PRIORITAS'
            },
            'LINKLIST_TAMBAH_VIP': {
                'judul': 'Linked List: pesanan VIP, masuk paling depan',
                'subjudul': 'insert: pesanan VIP langsung ke urutan pertama, O(1) di head.',
                'field': 'Nama pelanggan',
                'default': 'Pelanggan VIP',
                'btn': 'TAMBAH',
                'hint': 'nama untuk pesanan yang akan dibuat',
                'cmd': 'll_vip',
                'modul': 'M1 - rantai',
                'struktur': 'LINKLIST',
                'aksi': 'TAMBAH',
                'prioritas': 'VIP'
            },
            'LINKLIST_HAPUS': {
                'judul': 'Linked List: hapus pesanan ke-i',
                'subjudul': 'hapus: pesanan dicabut dari barisan, O(n) telusur.',
                'field': 'Indeks pesanan',
                'default': '0',
                'btn': 'HAPUS',
                'hint': 'indeks pesanan yang akan dicabut dari antrean',
                'cmd': 'll_delete',
                'modul': 'M1 - rantai',
                'struktur': 'LINKLIST',
                'aksi': 'HAPUS'
            },

            # --- M2: STACK DAN QUEUE ---
            'M2_STACK_POSTFIX': {
                'judul': 'Stack: hitung struk lewat postfix',
                'subjudul': 'Struk ditulis infix, lalu dihitung dua tahap dengan stack: tahap 1 infix menjadi postfix, tahap 2 postfix dievaluasi.',
                'field': 'Struk belanja (infix)',
                'default': '( 3 * 12000 ) + ( 2 * 8500 ) - 5000',
                'btn': 'HITUNG',
                'hint': 'angka, + - * / ^ dan tanda kurung; 3 x Rp12.000 dan 2 x Rp8.500, potongan Rp5.000',
                'cmd': 'stack_postfix',
                'modul': 'M2 - stack',
                'aksi': 'M2_STACK_POSTFIX'
            },
            'M2_STACK_UNDO': {
                'judul': 'Stack: Undo (Batalkan Perintah Terakhir)',
                'subjudul': 'undo_last: membatalkan aksi terakhir (LIFO) dan push ke redo.',
                'field': 'Aksi',
                'default': 'Batalkan aksi terakhir',
                'btn': 'UNDO',
                'hint': 'klik untuk membatalkan aksi enqueue atau dequeue terakhir',
                'cmd': 'stack_undo',
                'modul': 'M2 - stack',
                'aksi': 'M2_STACK_UNDO'
            },
            'M2_STACK_REDO': {
                'judul': 'Stack: Redo (Ulangi Aksi yang Dibatalkan)',
                'subjudul': 'redo_last: mengerjakan kembali aksi yang baru dibatalkan. Aksi baru mengosongkan redo.',
                'field': 'Aksi',
                'default': 'Ulangi aksi yang dibatalkan',
                'btn': 'REDO',
                'hint': 'klik untuk mengerjakan ulang aksi yang dibatalkan',
                'cmd': 'stack_redo',
                'modul': 'M2 - stack',
                'aksi': 'M2_STACK_REDO'
            },
            'M2_QUEUE_ENQUEUE': {
                'judul': 'Queue: tambah pesanan ke belakang (FIFO)',
                'subjudul': 'enqueue: pesanan baru masuk ke barisan paling belakang kedua antrean sekaligus, O(1).',
                'field': 'Nama pelanggan',
                'default': 'Pelanggan Baru',
                'btn': 'ENQUEUE',
                'hint': 'nama pelanggan untuk pesanan yang akan di-enqueue',
                'cmd': 'queue_enqueue',
                'modul': 'M2 - queue',
                'aksi': 'M2_QUEUE_ENQUEUE'
            },
            'M2_QUEUE_DEQUEUE_NAIF': {
                'judul': 'Queue Naif: layani pesanan dari depan (Larik Biasa)',
                'subjudul': 'dequeue: mengambil pesanan terdepan dan menggeser seluruh sisa elemen, O(n).',
                'field': 'Jumlah pesanan dilayani',
                'default': '1',
                'btn': 'DEQUEUE NAIF',
                'hint': 'masukkan jumlah pesanan yang ingin dilayani (misal: 1 atau 100)',
                'cmd': 'queue_dequeue_naive',
                'modul': 'M2 - queue naif',
                'aksi': 'M2_QUEUE_DEQUEUE_NAIF'
            },
            'M2_QUEUE_DEQUEUE_CIRCULAR': {
                'judul': 'Antrean Melingkar: layani pesanan dari depan (Circular Queue)',
                'subjudul': 'dequeue: memajukan front secara modular tanpa menggeser elemen, O(1).',
                'field': 'Jumlah pesanan dilayani',
                'default': '1',
                'btn': 'DEQUEUE CIRCULAR',
                'hint': 'masukkan jumlah pesanan yang ingin dilayani (misal: 1 atau 100)',
                'cmd': 'queue_dequeue_circular',
                'modul': 'M2 - circular',
                'aksi': 'M2_QUEUE_DEQUEUE_CIRCULAR'
            },

            # --- M3: SORT DAN SEARCH ---
            'M3_INSERTION_SORT': {
                'judul': 'Sort: Insertion Sort (Stabil, In-Place)',
                'subjudul': 'Mengurutkan pesanan dengan membandingkan dan menggeser ke kiri, O(n^2). Maksimal 20.000 baris.',
                'field': 'Kunci dan Jumlah baris (misal: harga 10)',
                'default': 'harga 10',
                'btn': 'SORT',
                'hint': 'pilihan kunci: oid, harga, selesai; maks 20.000 baris',
                'cmd': 'insertion_sort',
                'modul': 'M3 - sort',
                'aksi': 'M3_INSERTION_SORT'
            },
            'M3_MERGE_SORT': {
                'judul': 'Sort: Merge Sort (Stabil, Divide & Conquer)',
                'subjudul': 'Membelah data lalu menggabungkan kembali secara terurut, O(n log n). Sanggup 200.000 baris.',
                'field': 'Kunci dan Jumlah baris (misal: oid 4000)',
                'default': 'oid 4000',
                'btn': 'SORT',
                'hint': 'pilihan kunci: oid, harga, selesai; hingga 200.000 baris',
                'cmd': 'merge_sort',
                'modul': 'M3 - sort',
                'aksi': 'M3_MERGE_SORT'
            },
            'M3_LINEAR_SEARCH': {
                'judul': 'Search: Linear Search',
                'subjudul': 'Menelusuri satu per satu dari depan, tidak menuntut data terurut, O(n).',
                'field': 'Target OID',
                'default': 'O-137442',
                'btn': 'CARI',
                'hint': 'masukkan ID unik pesanan yang dicari',
                'cmd': 'linear_search',
                'modul': 'M3 - search',
                'aksi': 'M3_LINEAR_SEARCH'
            },
            'M3_BINARY_SEARCH': {
                'judul': 'Search: Binary Search',
                'subjudul': 'Membuang separuh sisa tiap langkah, data wajib terurut lebih dulu, O(log n).',
                'field': 'Target OID',
                'default': 'O-137442',
                'btn': 'CARI',
                'hint': 'masukkan ID unik pesanan yang dicari (terurut)',
                'cmd': 'binary_search',
                'modul': 'M3 - search',
                'aksi': 'M3_BINARY_SEARCH'
            }
        }

        self.menu_aktif = 'M2_STACK_POSTFIX'
        self.tombol_menu = {}

        # ================================================================
        # STRUKTUR LAYOUT:
        #   root
        #   |-- banner_atas (TOP)                 <- Header biru '2EZ4U Food Delivery'
        #   |-- panel_kiri  (LEFT)                <- Canvas scrollable daftar menu
        #   `-- frame_kanan (LEFT, fill=BOTH)     <- Parameter, Hasil, COMMAND, Catatan
        # ================================================================

        # --- BANNER ATAS (PERSIS MODUL) ---
        self.banner_atas = tk.Frame(root, bg="#1a365d", height=38)
        self.banner_atas.pack(side=tk.TOP, fill=tk.X)
        self.banner_atas.pack_propagate(False)

        tk.Label(
            self.banner_atas,
            text="2EZ4U Food Delivery",
            bg="#1a365d",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=12, pady=8)

        # --- PANEL KIRI DENGAN SCROLLBAR ---
        self.frame_kiri_kontainer = tk.Frame(root, bg="#e0e0e0", relief=tk.RIDGE, bd=1)
        self.frame_kiri_kontainer.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_kiri = tk.Canvas(self.frame_kiri_kontainer, bg="#e0e0e0", width=255, highlightthickness=0)
        self.scrollbar_kiri = tk.Scrollbar(self.frame_kiri_kontainer, orient="vertical", command=self.canvas_kiri.yview)

        self.frame_kiri = tk.Frame(self.canvas_kiri, bg="#e0e0e0")
        self.frame_kiri.bind("<Configure>", lambda e: self.canvas_kiri.configure(scrollregion=self.canvas_kiri.bbox("all")))

        self.canvas_kiri.create_window((0, 0), window=self.frame_kiri, anchor="nw")
        self.canvas_kiri.configure(yscrollcommand=self.scrollbar_kiri.set)

        self.canvas_kiri.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_kiri.pack(side=tk.RIGHT, fill=tk.Y)

        # Mousewheel scroll binding
        self.canvas_kiri.bind_all("<MouseWheel>", self._on_mousewheel)

        # SUSUNAN SEKSI MENU DI PANEL KIRI
        seksi_menu = [
            ("DATA", [
                ("DATA_LOAD", "Load")
            ]),
            ("M1 - DATA PESANAN", [
                ("ARRAY_LIHAT", "ARRAY - LIHAT PESANAN"),
                ("ARRAY_TAMBAH_REGULER", "ARRAY - TAMBAH PESANAN REGULER"),
                ("ARRAY_TAMBAH_PRIORITAS", "ARRAY - TAMBAH PESANAN PRIORITAS"),
                ("ARRAY_TAMBAH_VIP", "ARRAY - TAMBAH PESANAN VIP"),
                ("ARRAY_HAPUS", "ARRAY - HAPUS PESANAN"),
                ("LINKLIST_LIHAT", "LINKEDLIST - LIHAT PESANAN"),
                ("LINKLIST_TAMBAH_REGULER", "LINKEDLIST - TAMBAH PESANAN REGULER"),
                ("LINKLIST_TAMBAH_PRIORITAS", "LINKEDLIST - TAMBAH PESANAN PRIORITAS"),
                ("LINKLIST_TAMBAH_VIP", "LINKEDLIST - TAMBAH PESANAN VIP"),
                ("LINKLIST_HAPUS", "LINKEDLIST - HAPUS PESANAN"),
            ]),
            ("M2 - STACK DAN QUEUE", [
                ("M2_STACK_POSTFIX", "STACK - POSTFIX (MESIN KASIR)"),
                ("M2_STACK_UNDO", "STACK - UNDO"),
                ("M2_STACK_REDO", "STACK - REDO"),
                ("QUEUE_ENQUEUE", "QUEUE - ENQUEUE"),
                ("QUEUE_DEQUEUE_NAIF", "QUEUE - DEQUEUE NAIF"),
                ("QUEUE_DEQUEUE_CIRCULAR", "QUEUE - DEQUEUE CIRCULAR"),
            ]),
            ("M3 - SORT DAN SEARCH", [
                ("M3_INSERTION_SORT", "SORT - INSERTION SORT"),
                ("M3_MERGE_SORT", "SORT - MERGE SORT"),
                ("SEARCH_LINEAR_SEARCH", "SEARCH - LINEAR SEARCH"),
                ("SEARCH_BINARY_SEARCH", "SEARCH - BINARY SEARCH"),
            ])
        ]

        # Alias mapping untuk ID tombol yang sedikit beda nama di konfigurasi
        self.alias_id = {
            'QUEUE_ENQUEUE': 'M2_QUEUE_ENQUEUE',
            'QUEUE_DEQUEUE_NAIF': 'M2_QUEUE_DEQUEUE_NAIF',
            'QUEUE_DEQUEUE_CIRCULAR': 'M2_QUEUE_DEQUEUE_CIRCULAR',
            'SEARCH_LINEAR_SEARCH': 'M3_LINEAR_SEARCH',
            'SEARCH_BINARY_SEARCH': 'M3_BINARY_SEARCH',
        }

        for judul_seksi, items in seksi_menu:
            tk.Label(
                self.frame_kiri,
                text=judul_seksi,
                bg="#e0e0e0",
                font=("Arial", 8, "bold")
            ).pack(anchor="w", padx=6, pady=(8, 2))

            for item_id, teks in items:
                target_mid = self.alias_id.get(item_id, item_id)
                btn = tk.Button(
                    self.frame_kiri,
                    text=teks,
                    anchor="w",
                    font=("Arial", 8),
                    bg="#f0f0f0",
                    relief=tk.RAISED,
                    command=lambda mid=target_mid: self.pilih_menu(mid)
                )
                btn.pack(fill=tk.X, padx=5, pady=1)
                self.tombol_menu[target_mid] = btn

        # Indikator status di pojok kiri bawah (persis modul)
        self.btn_status = tk.Label(
            self.frame_kiri,
            text="[ siap ]",
            bg="#1a365d",
            fg="white",
            font=("Consolas", 8, "bold"),
            padx=10,
            pady=3,
            relief=tk.FLAT
        )
        self.btn_status.pack(anchor="w", padx=6, pady=(15, 12))

        # --- PANEL KANAN ---
        self.frame_kanan = tk.Frame(root, bg="white")
        self.frame_kanan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Parameter Dinamis (TOP)
        self.frame_form = tk.Frame(self.frame_kanan, bg="white")
        self.frame_form.pack(fill=tk.X, padx=20, pady=(12, 4))

        self.lbl_judul = tk.Label(
            self.frame_form,
            text="",
            bg="white",
            font=("Arial", 11, "bold"),
            anchor="w"
        )
        self.lbl_judul.pack(fill=tk.X)

        self.lbl_subjudul = tk.Label(
            self.frame_form,
            text="",
            bg="white",
            fg="#555555",
            font=("Arial", 8),
            anchor="w"
        )
        self.lbl_subjudul.pack(fill=tk.X, pady=(2, 8))

        # Baris Input Parameter
        self.frame_input_baris = tk.Frame(self.frame_form, bg="white")
        self.frame_input_baris.pack(fill=tk.X)

        self.lbl_param = tk.Label(
            self.frame_input_baris,
            text="",
            bg="white",
            font=("Arial", 9, "bold"),
            anchor="w"
        )
        self.lbl_param.pack(anchor="w")

        self.frame_input_aksi = tk.Frame(self.frame_input_baris, bg="white")
        self.frame_input_aksi.pack(anchor="w", pady=(3, 2))

        self.var_param = tk.StringVar()
        self.entry_param = tk.Entry(
            self.frame_input_aksi,
            textvariable=self.var_param,
            width=46,
            font=("Arial", 9)
        )
        self.entry_param.pack(side=tk.LEFT, ipady=3)
        self.entry_param.bind("<Return>", lambda event: self.eksekusi_aksi())

        self.btn_aksi = tk.Button(
            self.frame_input_aksi,
            text="",
            bg="#1a365d",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=22,
            pady=3,
            cursor="hand2",
            relief=tk.RAISED,
            command=self.eksekusi_aksi
        )
        self.btn_aksi.pack(side=tk.LEFT, padx=(14, 0))

        self.lbl_hint = tk.Label(
            self.frame_form,
            text="",
            bg="white",
            fg="#777777",
            font=("Arial", 8),
            anchor="w"
        )
        self.lbl_hint.pack(anchor="w", pady=(2, 0))

        # Garis pemisah horizontal
        tk.Frame(self.frame_kanan, height=1, bg="#e2e8f0").pack(fill=tk.X, padx=20, pady=(8, 6))

        # CATATAN PENJELAS DI BAWAH (BOTTOM)
        self.frame_catatan = tk.Frame(self.frame_kanan, bg="#f8f9fa", relief=tk.SOLID, bd=1)
        self.frame_catatan.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(0, 8))
        self.lbl_catatan_bawah = tk.Label(
            self.frame_catatan,
            text="Baris 1.x adalah tahap konversi, baris 2.x tahap evaluasi. Tahap 1 menahan operator di stack sampai gilirannya tiba. Tahap 2 menumpuk angka, dan setiap operator mengambil dua nilai teratas. Operand kanan selalu keluar lebih dulu.",
            bg="#f8f9fa",
            fg="#555555",
            font=("Arial", 8),
            justify=tk.LEFT,
            wraplength=760
        )
        self.lbl_catatan_bawah.pack(anchor="w", padx=8, pady=4)

        # COMMAND LOG (Tepat di atas catatan bawah)
        self.frame_bawah = tk.Frame(self.frame_kanan, height=85, bg="white", relief=tk.RIDGE, bd=1)
        self.frame_bawah.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(0, 6))
        self.frame_bawah.pack_propagate(False)

        tk.Label(
            self.frame_bawah,
            text="COMMAND",
            bg="white",
            font=("Arial", 8, "bold")
        ).pack(anchor="w", padx=5, pady=(2, 0))

        frame_log_inner = tk.Frame(self.frame_bawah, bg="white")
        frame_log_inner.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 4))

        scroll_log = tk.Scrollbar(frame_log_inner)
        self.text_command = tk.Text(
            frame_log_inner,
            fg="black",
            bg="white",
            font=("Consolas", 9),
            yscrollcommand=scroll_log.set
        )
        scroll_log.config(command=self.text_command.yview)
        scroll_log.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_command.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # OUTPUT HASIL (MIDDLE - sisa ruang di tengah)
        frame_hasil_wrap = tk.Frame(self.frame_kanan, bg="white")
        frame_hasil_wrap.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 6))

        scroll_hasil = tk.Scrollbar(frame_hasil_wrap)
        self.text_hasil = tk.Text(
            frame_hasil_wrap,
            font=("Consolas", 9),
            bg="white",
            relief=tk.SOLID,
            bd=1,
            yscrollcommand=scroll_hasil.set
        )
        scroll_hasil.config(command=self.text_hasil.yview)
        scroll_hasil.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_hasil.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tampilkan menu default: STACK - POSTFIX (MESIN KASIR) seperti modul
        self.pilih_menu(self.menu_aktif)

    def _on_mousewheel(self, event):
        try:
            self.canvas_kiri.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    # =====================================================================
    # LOGIKA NAVIGASI MENU DINAMIS
    # =====================================================================

    def pilih_menu(self, menu_id):
        """Memilih menu navigasi dan menyesuaikan form parameter di panel kanan."""
        if menu_id not in self.menu_config:
            return

        self.menu_aktif = menu_id
        config = self.menu_config[menu_id]

        # Update tampilan judul, parameter, tombol aksi, dan hint
        self.lbl_judul.config(text=config['judul'])
        self.lbl_subjudul.config(text=config['subjudul'])
        self.lbl_param.config(text=config['field'])
        self.btn_aksi.config(text=config['btn'])
        self.lbl_hint.config(text=config['hint'])
        self.var_param.set(config['default'])

        # Highlight tombol menu yang sedang aktif
        for mid, btn in self.tombol_menu.items():
            if mid == menu_id:
                btn.config(relief=tk.SUNKEN, bg="#c8d6e5")
            else:
                btn.config(relief=tk.RAISED, bg="#f0f0f0")

        self.entry_param.focus_set()
        self.entry_param.select_range(0, tk.END)

    # =====================================================================
    # UTILITAS M3
    # =====================================================================

    def _pastikan_data_m3(self):
        if self.backend_array.ukuran == 0:
            self.aksi_load()
        return self.backend_array.ukuran > 0

    def _parse_param_sort_m3(self):
        bagian = self.var_param.get().strip().split()
        if len(bagian) == 0:
            return None, 0

        kunci = normalisasi_kunci(bagian[0])
        if kunci is None:
            messagebox.showerror("Error", "Kunci harus salah satu dari: oid, harga, selesai.")
            return None, 0

        jumlah = self.backend_array.ukuran
        if len(bagian) >= 2:
            try:
                jumlah = int(bagian[1])
            except ValueError:
                messagebox.showerror("Error", "Jumlah baris harus berupa bilangan bulat.")
                return None, 0

        if jumlah < 0:
            jumlah = 0
        if jumlah > self.backend_array.ukuran:
            jumlah = self.backend_array.ukuran
        return kunci, jumlah

    def _ambil_larik_array_m3(self, jumlah):
        data = [None] * jumlah
        for i in range(jumlah):
            data[i] = self.backend_array.get(i)
        return data

    def _format_pesanan_ringkas(self, pesanan):
        if pesanan is None:
            return "-"
        oid = pesanan[0] if len(pesanan) > 0 else ""
        pelanggan = pesanan[1] if len(pesanan) > 1 else ""
        menu = pesanan[3] if len(pesanan) > 3 else ""
        harga = pesanan[4] if len(pesanan) > 4 else ""
        selesai = pesanan[7] if len(pesanan) > 7 else ""
        status = pesanan[8] if len(pesanan) > 8 else ""
        if selesai == "":
            selesai = "-"
        return f"{oid:<10} {pelanggan[:20]:<20} {menu[:18]:<18} {harga:>8} {selesai:>8} {status:<8}"

    def _format_sampel_m3(self, data, batas=10):
        jumlah = len(data)
        if jumlah < batas:
            batas = jumlah

        teks = f"{'OID':<10} {'Pelanggan':<20} {'Menu':<18} {'Harga':>8} {'Selesai':>8} {'Status':<8}\n"
        teks += "-" * 82 + "\n"
        for i in range(batas):
            teks += self._format_pesanan_ringkas(data[i]) + "\n"
        return teks
    # =====================================================================
    # EKSEKUSI OPERASI BACKEND
    # =====================================================================

    def eksekusi_aksi(self):
        """Mengeksekusi operasi sesuai menu yang sedang dipilih."""
        config = self.menu_config[self.menu_aktif]
        aksi = config['aksi']

        # -------------------------------------------------------------
        # FITUR DATA
        # -------------------------------------------------------------
        if aksi == 'DATA_LOAD':
            self.aksi_load()
            return

        # -------------------------------------------------------------
        # FITUR M1
        # -------------------------------------------------------------
        elif aksi == 'TAMBAH':
            target_ds = self.backend_array if config['struktur'] == 'ARRAY' else self.backend_ll
            nama = self.var_param.get().strip() or "Pelanggan Baru"
            prioritas = config['prioritas']
            nilai_prioritas = "1" if prioritas == "VIP" else "2" if prioritas == "PRIORITAS" else "3"
            oid_baru = f"O-{200000 + target_ds.ukuran + 1}"
            pesanan_baru = [oid_baru, nama, "Mie Gacoan", "Mie Hompimpa Level 2, Udang Keju", "15000", nilai_prioritas, "45000", "", "ANTRE"]

            mulai = time.perf_counter()
            if prioritas == "REGULER":
                target_ds.append(pesanan_baru)
                posisi_teks = "paling belakang"
            elif prioritas == "PRIORITAS":
                indeks_tengah = target_ds.ukuran // 2
                target_ds.insert(indeks_tengah, pesanan_baru)
                posisi_teks = f"tengah (indeks {indeks_tengah})"
            elif prioritas == "VIP":
                target_ds.insert(0, pesanan_baru)
                posisi_teks = "paling depan (indeks 0)"
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"[{config['struktur']}] Sukses menambahkan pesanan {prioritas} ke posisi {posisi_teks}.\n"
                f"Total pesanan saat ini: {target_ds.ukuran:,}\n\n"
                f"Data pesanan baru:\n{pesanan_baru}"
            )

        elif aksi == 'LIHAT':
            target_ds = self.backend_array if config['struktur'] == 'ARRAY' else self.backend_ll
            try:
                indeks = int(self.var_param.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Indeks harus berupa bilangan bulat.")
                return

            mulai = time.perf_counter()
            hasil = target_ds.get(indeks)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            if hasil is not None:
                self.text_hasil.insert(
                    tk.END,
                    f"DATA DITEMUKAN PADA INDEKS {indeks} [{config['struktur']}]:\n"
                    f"{hasil}\n\n"
                    f"Total pesanan tersimpan: {target_ds.ukuran:,}"
                )
            else:
                self.text_hasil.insert(
                    tk.END,
                    f"DATA TIDAK DITEMUKAN / INDEKS {indeks} DI LUAR BATAS!\n"
                    f"Rentang indeks yang valid: 0 s.d. {max(0, target_ds.ukuran - 1):,}"
                )

        elif aksi == 'HAPUS':
            target_ds = self.backend_array if config['struktur'] == 'ARRAY' else self.backend_ll
            try:
                indeks = int(self.var_param.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Indeks harus berupa bilangan bulat.")
                return

            mulai = time.perf_counter()
            dihapus = target_ds.hapus(indeks)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            if dihapus is not None:
                self.text_hasil.insert(
                    tk.END,
                    f"DATA BERHASIL DIHAPUS DARI INDEKS {indeks} [{config['struktur']}]:\n"
                    f"{dihapus}\n\n"
                    f"Sisa total pesanan: {target_ds.ukuran:,}"
                )
            else:
                self.text_hasil.insert(
                    tk.END,
                    f"GAGAL MENGHAPUS / INDEKS {indeks} DI LUAR BATAS!\n"
                    f"Rentang indeks yang valid: 0 s.d. {max(0, target_ds.ukuran - 1):,}"
                )

        # -------------------------------------------------------------
        # FITUR M2: STACK & QUEUE
        # -------------------------------------------------------------
        elif aksi == 'M2_STACK_POSTFIX':
            ekspresi = self.var_param.get().strip()
            mulai = time.perf_counter()
            try:
                postfix_list, langkah_konv = ke_postfix(ekspresi)
                total, langkah_eval = hitung(postfix_list)
                selesai = time.perf_counter()
                waktu_ms = (selesai - mulai) * 1000

                # Format ringkasan atas persis seperti modul
                hasil_teks = f"Struk : {ekspresi}\n"
                hasil_teks += f"Postfix: {' '.join(postfix_list)}\n"
                hasil_teks += f"TOTAL : Rp {total:,.0f}".replace(",", ".") + "\n\n"

                # Header Tabel
                hasil_teks += f"{'langkah':<10} {'token':<8} {'tindakan':<38} {'stack':<18} {'output'}\n"
                hasil_teks += "-" * 105 + "\n"

                # Baris 1.x: Konversi Infix -> Postfix
                for no, tok, act, st, out in langkah_konv:
                    hasil_teks += f"{no:<10} {tok:<8} {act:<38} {st:<18} {out}\n"

                # Baris 2.x: Evaluasi Postfix
                for no, tok, act, st in langkah_eval:
                    hasil_teks += f"{no:<10} {tok:<8} {act:<38} {st:<18}\n"

                self.text_hasil.delete(1.0, tk.END)
                self.text_hasil.insert(tk.END, hasil_teks)

                self.lbl_catatan_bawah.config(
                    text="Baris 1.x adalah tahap konversi, baris 2.x tahap evaluasi. Tahap 1 menahan operator di stack sampai gilirannya tiba. Tahap 2 menumpuk angka, dan setiap operator mengambil dua nilai teratas. Operand kanan selalu keluar lebih dulu."
                )

            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengevaluasi ekspresi: {e}")
                return

        elif aksi == 'M2_QUEUE_ENQUEUE':
            nama = self.var_param.get().strip() or "Pelanggan Baru"
            oid_baru = f"O-{200000 + self.queue_circular.size() + 1}"
            pesanan_baru = [oid_baru, nama, "Resto Cepat", "Paket Antrean", "20000", "3", "50000", "", "ANTRE"]

            mulai = time.perf_counter()
            self.queue_naif.enqueue(pesanan_baru)
            self.queue_circular.enqueue(pesanan_baru)
            self.manajer_undo.catat_aksi('ENQUEUE', pesanan_baru)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"Pesanan {oid_baru} ({nama}) berhasil masuk paling belakang KEDUA antrean.\n"
                f"Panjang antrean Naif: {self.queue_naif.ukuran:,} | Circular: {self.queue_circular.count:,}\n\n"
                f"Data: {pesanan_baru}"
            )

        elif aksi == 'M2_QUEUE_DEQUEUE_NAIF':
            try:
                k = int(self.var_param.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa bilangan bulat.")
                return

            mulai = time.perf_counter()
            keluar, digeser = self.queue_naif.dequeue(k)
            if keluar:
                self.queue_circular.dequeue(len(keluar))
                self.manajer_undo.catat_aksi('DEQUEUE', keluar)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"{len(keluar)} pesanan keluar dari antrean Naif.\n"
                f"{digeser:,} elemen digeser di memori (O(n) per layanan)!\n"
                f"Sisa antrean Naif: {self.queue_naif.ukuran:,} | Circular: {self.queue_circular.count:,}\n\n"
                f"Sampel pesanan pertama yang dilayani: {keluar[0] if keluar else 'None'}"
            )

        elif aksi == 'M2_QUEUE_DEQUEUE_CIRCULAR':
            try:
                k = int(self.var_param.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa bilangan bulat.")
                return

            mulai = time.perf_counter()
            keluar, digeser = self.queue_circular.dequeue(k)
            if keluar:
                self.queue_naif.dequeue(len(keluar))
                self.manajer_undo.catat_aksi('DEQUEUE', keluar)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"{len(keluar)} pesanan keluar dari Antrean Melingkar (Circular Queue).\n"
                f"0 elemen digeser (front bergeser modular ke {self.queue_circular.front})! O(1)\n"
                f"Sisa antrean Circular: {self.queue_circular.count:,} | Naif: {self.queue_naif.ukuran:,}\n\n"
                f"Sampel pesanan pertama yang dilayani: {keluar[0] if keluar else 'None'}"
            )

        elif aksi == 'M2_STACK_UNDO':
            mulai = time.perf_counter()
            pesan = self.manajer_undo.undo(self.queue_circular, self.queue_naif)
            undo_sz, redo_sz = self.manajer_undo.stats()
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"HASIL UNDO:\n{pesan}\n\n"
                f"Panjang antrean Naif: {self.queue_naif.ukuran:,} | Circular: {self.queue_circular.count:,}\n"
                f"Status tumpukan: Undo={undo_sz}, Redo={redo_sz}"
            )

        elif aksi == 'M2_STACK_REDO':
            mulai = time.perf_counter()
            pesan = self.manajer_undo.redo(self.queue_circular, self.queue_naif)
            undo_sz, redo_sz = self.manajer_undo.stats()
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"HASIL REDO:\n{pesan}\n\n"
                f"Panjang antrean Naif: {self.queue_naif.ukuran:,} | Circular: {self.queue_circular.count:,}\n"
                f"Status tumpukan: Undo={undo_sz}, Redo={redo_sz}"
            )

        # -------------------------------------------------------------
        # FITUR M3: SORTING & SEARCHING
        # -------------------------------------------------------------
        elif aksi == 'M3_INSERTION_SORT':
            if not self._pastikan_data_m3():
                return
            kunci, jumlah = self._parse_param_sort_m3()
            if kunci is None:
                return
            if jumlah > 20000:
                messagebox.showwarning("Batas Insertion Sort", "Insertion Sort dibatasi maksimal 20.000 baris agar UI tidak membeku. Pakai Merge Sort untuk data besar.")
                return

            data = self._ambil_larik_array_m3(jumlah)
            mulai = time.perf_counter()
            hasil, perbandingan, pemindahan = m3_insertion_sort(data, kunci)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            hasil_teks = "SORT - INSERTION SORT\n"
            hasil_teks += f"Kunci       : {kunci}\n"
            hasil_teks += f"Jumlah data : {jumlah:,}\n"
            hasil_teks += f"Perbandingan: {perbandingan:,}\n"
            hasil_teks += f"Pemindahan  : {pemindahan:,}\n"
            hasil_teks += "Kompleksitas: O(n^2), stabil karena elemen berkunci sama tidak disalip.\n\n"
            hasil_teks += "Sampel 10 baris pertama setelah sort:\n"
            hasil_teks += self._format_sampel_m3(hasil)

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(tk.END, hasil_teks)
            self.lbl_catatan_bawah.config(text="M3 wajib menampilkan jumlah perbandingan. Insertion Sort cocok untuk data kecil atau hampir terurut, dan ditolak untuk data terlalu besar agar aplikasi tidak membeku.")

        elif aksi == 'M3_MERGE_SORT':
            if not self._pastikan_data_m3():
                return
            kunci, jumlah = self._parse_param_sort_m3()
            if kunci is None:
                return

            data = self._ambil_larik_array_m3(jumlah)
            mulai = time.perf_counter()
            hasil, perbandingan, pemindahan = m3_merge_sort(data, kunci)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            hasil_teks = "SORT - MERGE SORT\n"
            hasil_teks += f"Kunci       : {kunci}\n"
            hasil_teks += f"Jumlah data : {jumlah:,}\n"
            hasil_teks += f"Perbandingan: {perbandingan:,}\n"
            hasil_teks += f"Pemindahan  : {pemindahan:,}\n"
            hasil_teks += "Kompleksitas: O(n log n), stabil karena saat kunci sama bagian kiri didahulukan.\n\n"
            hasil_teks += "Sampel 10 baris pertama setelah sort:\n"
            hasil_teks += self._format_sampel_m3(hasil)

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(tk.END, hasil_teks)
            self.lbl_catatan_bawah.config(text="Merge Sort dipakai untuk data besar. Jumlah perbandingan tumbuh sekitar n log n, sehingga aman untuk 200.000 baris.")

        elif aksi == 'M3_LINEAR_SEARCH':
            if not self._pastikan_data_m3():
                return
            target = self.var_param.get().strip()
            if target == "":
                messagebox.showerror("Error", "Target OID tidak boleh kosong.")
                return

            data = self._ambil_larik_array_m3(self.backend_array.ukuran)
            mulai = time.perf_counter()
            indeks, pesanan, perbandingan = m3_linear_search(data, target)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            hasil_teks = "SEARCH - LINEAR SEARCH\n"
            hasil_teks += f"Target      : {target}\n"
            hasil_teks += f"Jumlah data : {len(data):,}\n"
            hasil_teks += f"Perbandingan: {perbandingan:,}\n"
            hasil_teks += "Kompleksitas: O(n), tidak perlu data terurut.\n\n"
            if indeks >= 0:
                hasil_teks += f"Ditemukan di indeks asli {indeks:,}:\n"
                hasil_teks += self._format_pesanan_ringkas(pesanan) + "\n"
            else:
                hasil_teks += "Data tidak ditemukan.\n"

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(tk.END, hasil_teks)
            self.lbl_catatan_bawah.config(text="Linear Search menelusuri dari depan dan cocok untuk pencarian satu-dua kali tanpa biaya pengurutan awal.")

        elif aksi == 'M3_BINARY_SEARCH':
            if not self._pastikan_data_m3():
                return
            target = self.var_param.get().strip()
            if target == "":
                messagebox.showerror("Error", "Target OID tidak boleh kosong.")
                return

            data = self._ambil_larik_array_m3(self.backend_array.ukuran)
            mulai = time.perf_counter()
            mulai_sort = time.perf_counter()
            terurut, perbandingan_sort, pemindahan_sort = m3_merge_sort(data, "oid")
            selesai_sort = time.perf_counter()
            indeks, pesanan, perbandingan_cari = m3_binary_search(terurut, target)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000
            waktu_sort_ms = (selesai_sort - mulai_sort) * 1000
            waktu_cari_ms = (selesai - selesai_sort) * 1000

            hasil_teks = "SEARCH - BINARY SEARCH\n"
            hasil_teks += f"Target       : {target}\n"
            hasil_teks += f"Jumlah data  : {len(data):,}\n"
            hasil_teks += f"Pra-sort OID : Merge Sort {waktu_sort_ms:.2f} ms | {perbandingan_sort:,} perbandingan | {pemindahan_sort:,} pemindahan\n"
            hasil_teks += f"Pencarian    : {waktu_cari_ms:.2f} ms | {perbandingan_cari:,} perbandingan\n"
            hasil_teks += "Kompleksitas : sort O(n log n) sekali, lalu cari O(log n).\n\n"
            if indeks >= 0:
                hasil_teks += f"Ditemukan di indeks data terurut {indeks:,}:\n"
                hasil_teks += self._format_pesanan_ringkas(pesanan) + "\n"
            else:
                hasil_teks += "Data tidak ditemukan.\n"

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(tk.END, hasil_teks)
            self.lbl_catatan_bawah.config(text="Binary Search hanya sah pada data yang sudah terurut menurut OID. Karena itu UI mencatat biaya Merge Sort awal secara terang-terangan.")

        # Catat ke panel COMMAND dengan format modul: [perintah] -> [modul] [waktu] ms
        pesan_log = f"{config['cmd']:<22} -> {config['modul']:<14} {waktu_ms:.2f} ms\n"
        self.text_command.insert(tk.END, pesan_log)
        self.text_command.see(tk.END)

        # Update indikator status di pojok kiri bawah
        self.btn_status.config(text=f"[{config['modul']}]  {waktu_ms:.2f} ms")

    # =====================================================================
    # FUNGSI DATA
    # =====================================================================

    def aksi_load(self):
        """Memuat dataset CSV ke dalam Array dan Linked List."""
        mulai = time.perf_counter()

        # Reset struktur data agar tidak menumpuk saat Load ditekan berulang
        self.backend_array.ukuran = 0
        self.backend_array.kapasitas = 4
        self.backend_array.data = [None] * self.backend_array.kapasitas

        self.backend_ll.head = None
        self.backend_ll.tail = None
        self.backend_ll.ukuran = 0

        self.queue_naif.clear()
        self.queue_circular.clear()

        jumlah = 0
        jumlah_antre = 0
        try:
            with open('data/pesanan.csv', 'r') as file:
                header = file.readline()
                for baris in file:
                    elemen = baris.strip().split(',')
                    self.backend_array.append(elemen)
                    self.backend_ll.append(elemen)
                    if len(elemen) >= 9 and elemen[8] == 'ANTRE':
                        self.queue_naif.enqueue(elemen)
                        self.queue_circular.enqueue(elemen)
                        jumlah_antre += 1
                    jumlah += 1

            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"DATA BERHASIL DIMUAT:\n"
                f"Total {jumlah:,} baris pesanan dimuat ke Array dan Linked List.\n"
                f"Total {jumlah_antre:,} pesanan berstatus ANTRE siap diuji di antrean M2."
            )

            # Format log COMMAND: load -> M1 - larik {waktu} ms
            pesan_log = f"{'load':<22} -> {'M1 - larik':<14} {waktu_ms:.2f} ms\n"
            self.text_command.insert(tk.END, pesan_log)
            self.text_command.see(tk.END)

            self.btn_status.config(text=f"[M1 - larik]  {waktu_ms:.2f} ms")

        except FileNotFoundError:
            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(tk.END, "Error: File data/pesanan.csv tidak ditemukan!")
            pesan_log = f"{'load':<22} -> {'M1 - larik':<14} GAGAL\n"
            self.text_command.insert(tk.END, pesan_log)
            self.text_command.see(tk.END)








