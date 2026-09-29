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

class AppUI:
    def __init__(self, root, backend_array, backend_ll, queue_naif=None, queue_circular=None, manajer_undo=None):
        self.root = root
        self.backend_array = backend_array
        self.backend_ll = backend_ll
        self.queue_naif = queue_naif if queue_naif is not None else QueueNaif()
        self.queue_circular = queue_circular if queue_circular is not None else AntreanMelingkar()
        self.manajer_undo = manajer_undo if manajer_undo is not None else ManajerUndoRedo()

        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1050x650")

        # ================================================================
        # KONFIGURASI MENU DAN PARAMETER FORM (M1 & M2)
        # ================================================================
        self.menu_config = {
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

            # --- M2: STACK & QUEUE ---
            'M2_ISI_ANTREAN': {
                'judul': 'Queue: isi antrean dari pesanan berstatus ANTRE',
                'subjudul': 'Memuat pesanan berstatus ANTRE dari pesanan.csv ke Antrean Naif dan Circular.',
                'field': 'Status data',
                'default': 'data/pesanan.csv',
                'btn': 'ISI ANTREAN',
                'hint': 'klik untuk memuat seluruh pesanan berstatus ANTRE ke kedua antrean',
                'cmd': 'queue_init',
                'modul': 'M2 - queue',
                'aksi': 'M2_ISI_ANTREAN'
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
            'M2_STACK_POSTFIX': {
                'judul': 'Stack Postfix (Mesin Kasir)',
                'subjudul': 'Konversi infix -> postfix dan evaluasi bertahap untuk menghitung struk kasir.',
                'field': 'Ekspresi struk kasir',
                'default': '( 3 * 12000 ) + ( 2 * 8500 ) - 5000',
                'btn': 'HITUNG STRUK',
                'hint': 'contoh: ( 3 * 12000 ) + ( 2 * 8500 ) - 5000',
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
        }

        self.menu_aktif = 'ARRAY_TAMBAH_REGULER'
        self.tombol_menu = {}

        # ================================================================
        # STRUKTUR LAYOUT:
        #   root
        #   ├── banner_atas (TOP)                 ← Header biru '2EZ4U Food Delivery'
        #   ├── panel_kiri  (LEFT)                ← Canvas scrollable daftar menu
        #   └── frame_kanan (LEFT, fill=BOTH)     ← Parameter, Hasil, COMMAND
        # ================================================================

        # --- BANNER ATAS (PERSIS MODUL) ---
        self.banner_atas = tk.Frame(root, bg="#1a365d", height=36)
        self.banner_atas.pack(side=tk.TOP, fill=tk.X)
        self.banner_atas.pack_propagate(False)

        tk.Label(
            self.banner_atas,
            text="2EZ4U Food Delivery",
            bg="#1a365d",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=12, pady=6)

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

        # === DATA ===
        tk.Label(self.frame_kiri, text="DATA", bg="#e0e0e0",
                 font=("Arial", 9, "bold")).pack(anchor="w", padx=5, pady=(8, 2))
        btn_load = tk.Button(self.frame_kiri, text="Load", anchor="w",
                             command=self.aksi_load)
        btn_load.pack(fill=tk.X, padx=5, pady=1)

        # === M1 - DATA PESANAN ===
        tk.Label(self.frame_kiri, text="M1 - DATA PESANAN", bg="#e0e0e0",
                 font=("Arial", 9, "bold")).pack(anchor="w", padx=5, pady=(8, 2))

        daftar_menu_m1 = [
            ('ARRAY_LIHAT', 'ARRAY - LIHAT PESANAN'),
            ('ARRAY_TAMBAH_REGULER', 'ARRAY - TAMBAH PESANAN REGULER'),
            ('ARRAY_TAMBAH_PRIORITAS', 'ARRAY - TAMBAH PESANAN PRIORITAS'),
            ('ARRAY_TAMBAH_VIP', 'ARRAY - TAMBAH PESANAN VIP'),
            ('ARRAY_HAPUS', 'ARRAY - HAPUS PESANAN'),
            ('LINKLIST_LIHAT', 'LINKEDLIST - LIHAT PESANAN'),
            ('LINKLIST_TAMBAH_REGULER', 'LINKEDLIST - TAMBAH PESANAN REGULER'),
            ('LINKLIST_TAMBAH_PRIORITAS', 'LINKEDLIST - TAMBAH PESANAN PRIORITAS'),
            ('LINKLIST_TAMBAH_VIP', 'LINKEDLIST - TAMBAH PESANAN VIP'),
            ('LINKLIST_HAPUS', 'LINKEDLIST - HAPUS PESANAN'),
        ]

        for menu_id, teks in daftar_menu_m1:
            btn = tk.Button(
                self.frame_kiri,
                text=teks,
                anchor="w",
                command=lambda mid=menu_id: self.pilih_menu(mid)
            )
            btn.pack(fill=tk.X, padx=5, pady=1)
            self.tombol_menu[menu_id] = btn

        # === M2 - ANTREAN DAN UNDO ===
        tk.Label(self.frame_kiri, text="M2 - ANTREAN DAN UNDO", bg="#e0e0e0",
                 font=("Arial", 9, "bold")).pack(anchor="w", padx=5, pady=(10, 2))

        daftar_menu_m2 = [
            ('M2_ISI_ANTREAN', 'Isi antrean FIFO'),
            ('M2_QUEUE_ENQUEUE', 'QUEUE - ENQUEUE'),
            ('M2_QUEUE_DEQUEUE_NAIF', 'QUEUE - DEQUEUE NAIF'),
            ('M2_QUEUE_DEQUEUE_CIRCULAR', 'QUEUE - DEQUEUE CIRCULAR'),
            ('M2_STACK_POSTFIX', 'STACK - POSTFIX (MESIN KASIR)'),
            ('M2_STACK_UNDO', 'Undo'),
            ('M2_STACK_REDO', 'Redo'),
        ]

        for menu_id, teks in daftar_menu_m2:
            btn = tk.Button(
                self.frame_kiri,
                text=teks,
                anchor="w",
                command=lambda mid=menu_id: self.pilih_menu(mid)
            )
            btn.pack(fill=tk.X, padx=5, pady=1)
            self.tombol_menu[menu_id] = btn

        # Indikator status di pojok kiri bawah (seperti modul)
        self.btn_status = tk.Button(
            self.frame_kiri,
            text="siap",
            bg="#1a365d",
            fg="white",
            font=("Arial", 8, "bold"),
            padx=10,
            pady=2,
            relief=tk.FLAT
        )
        self.btn_status.pack(anchor="w", padx=5, pady=(15, 10))

        # --- PANEL KANAN ---
        self.frame_kanan = tk.Frame(root, bg="white")
        self.frame_kanan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Parameter Dinamis (TOP)
        self.frame_form = tk.Frame(self.frame_kanan, bg="white")
        self.frame_form.pack(fill=tk.X, padx=20, pady=(15, 5))

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
            font=("Arial", 9),
            anchor="w"
        )
        self.lbl_subjudul.pack(fill=tk.X, pady=(2, 10))

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
            width=36,
            font=("Arial", 10)
        )
        self.entry_param.pack(side=tk.LEFT, ipady=3)
        self.entry_param.bind("<Return>", lambda event: self.eksekusi_aksi())

        self.btn_aksi = tk.Button(
            self.frame_input_aksi,
            text="",
            bg="#1a365d",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=18,
            pady=3,
            cursor="hand2",
            relief=tk.RAISED,
            command=self.eksekusi_aksi
        )
        self.btn_aksi.pack(side=tk.LEFT, padx=(12, 0))

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
        tk.Frame(self.frame_kanan, height=1, bg="#e2e8f0").pack(fill=tk.X, padx=20, pady=(10, 8))

        # COMMAND LOG (BOTTOM)
        self.frame_bawah = tk.Frame(self.frame_kanan, height=120, bg="white", relief=tk.RIDGE, bd=1)
        self.frame_bawah.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(0, 10))
        self.frame_bawah.pack_propagate(False)

        tk.Label(
            self.frame_bawah,
            text="COMMAND",
            bg="white",
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=5, pady=(3, 0))

        frame_log_inner = tk.Frame(self.frame_bawah, bg="white")
        frame_log_inner.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        scroll_log = tk.Scrollbar(frame_log_inner)
        self.text_command = tk.Text(
            frame_log_inner,
            fg="black",
            bg="white",
            font=("Consolas", 10),
            yscrollcommand=scroll_log.set
        )
        scroll_log.config(command=self.text_command.yview)
        scroll_log.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_command.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # OUTPUT HASIL (MIDDLE - sisa ruang)
        frame_hasil_wrap = tk.Frame(self.frame_kanan, bg="white")
        frame_hasil_wrap.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        scroll_hasil = tk.Scrollbar(frame_hasil_wrap)
        self.text_hasil = tk.Text(
            frame_hasil_wrap,
            font=("Consolas", 10),
            yscrollcommand=scroll_hasil.set
        )
        scroll_hasil.config(command=self.text_hasil.yview)
        scroll_hasil.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_hasil.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tampilkan menu default: ARRAY - TAMBAH PESANAN REGULER
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
                btn.config(relief=tk.RAISED, bg="#e0e0e0")

        self.entry_param.focus_set()
        self.entry_param.select_range(0, tk.END)

    # =====================================================================
    # EKSEKUSI OPERASI BACKEND (M1 & M2)
    # =====================================================================

    def eksekusi_aksi(self):
        """Mengeksekusi operasi sesuai menu yang sedang dipilih."""
        config = self.menu_config[self.menu_aktif]
        aksi = config['aksi']

        # -------------------------------------------------------------
        # FITUR M1
        # -------------------------------------------------------------
        if aksi == 'TAMBAH':
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
        # FITUR M2: QUEUE & STACK
        # -------------------------------------------------------------
        elif aksi == 'M2_ISI_ANTREAN':
            mulai = time.perf_counter()
            self.queue_naif.clear()
            self.queue_circular.clear()

            count = 0
            try:
                with open('data/pesanan.csv', 'r') as f:
                    _ = f.readline()
                    for line in f:
                        row = line.strip().split(',')
                        if len(row) >= 9 and row[8] == 'ANTRE':
                            self.queue_naif.enqueue(row)
                            self.queue_circular.enqueue(row)
                            count += 1
                selesai = time.perf_counter()
                waktu_ms = (selesai - mulai) * 1000

                self.text_hasil.delete(1.0, tk.END)
                self.text_hasil.insert(
                    tk.END,
                    f"{count:,} pesanan berstatus ANTRE masuk ke KEDUA antrean (Naif dan Circular).\n"
                    f"Panjang antrean Naif: {self.queue_naif.ukuran:,} | Circular: {self.queue_circular.count:,}\n\n"
                    f"Sistem antrean M2 siap diuji untuk operasi Enqueue dan Dequeue."
                )
            except FileNotFoundError:
                messagebox.showerror("Error", "File data/pesanan.csv tidak ditemukan!")
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
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"{len(keluar)} pesanan keluar dari antrean Naif.\n"
                f"{digeser:,} elemen digeser di memori (O(n) per layanan)!\n"
                f"Sisa antrean Naif: {self.queue_naif.ukuran:,}\n\n"
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
                self.manajer_undo.catat_aksi('DEQUEUE', keluar)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"{len(keluar)} pesanan keluar dari Antrean Melingkar (Circular Queue).\n"
                f"0 elemen digeser (front bergeser modular ke {self.queue_circular.front})! O(1)\n"
                f"Sisa antrean Circular: {self.queue_circular.count:,}\n\n"
                f"Sampel pesanan pertama yang dilayani: {keluar[0] if keluar else 'None'}"
            )

        elif aksi == 'M2_STACK_POSTFIX':
            ekspresi = self.var_param.get().strip()
            mulai = time.perf_counter()
            try:
                postfix_list, langkah_konv = ke_postfix(ekspresi)
                total, langkah_eval = hitung(postfix_list)
                selesai = time.perf_counter()
                waktu_ms = (selesai - mulai) * 1000

                hasil_teks = f"STRUK KASIR (INFIX -> POSTFIX -> EVALUASI)\n"
                hasil_teks += f"Ekspresi Infix: {ekspresi}\n"
                hasil_teks += f"Postfix: {' '.join(postfix_list)}\n\n"

                hasil_teks += "Tahap 1: Konversi Infix -> Postfix\n"
                hasil_teks += f"{'token':<8} {'tindakan':<30} {'stack':<15} {'keluaran':<30}\n"
                hasil_teks += "-" * 85 + "\n"
                for t, act, st, out in langkah_konv:
                    hasil_teks += f"{t:<8} {act:<30} {st:<15} {out:<30}\n"

                hasil_teks += "\nTahap 2: Evaluasi Postfix\n"
                hasil_teks += f"{'token':<8} {'tindakan':<42} {'stack nilai':<25}\n"
                hasil_teks += "-" * 75 + "\n"
                for t, act, st in langkah_eval:
                    hasil_teks += f"{t:<8} {act:<42} {st:<25}\n"

                hasil_teks += "\n" + "=" * 50 + "\n"
                hasil_teks += f"TOTAL STRUK: Rp {total:,}\n"
                hasil_teks += "=" * 50 + "\n"

                self.text_hasil.delete(1.0, tk.END)
                self.text_hasil.insert(tk.END, hasil_teks)

            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengevaluasi ekspresi: {e}")
                return

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
                f"Panjang antrean Circular saat ini: {self.queue_circular.count:,}\n"
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
                f"Panjang antrean Circular saat ini: {self.queue_circular.count:,}\n"
                f"Status tumpukan: Undo={undo_sz}, Redo={redo_sz}"
            )

        # Catat ke panel COMMAND dengan format modul: [perintah] -> [modul] [waktu] ms
        pesan_log = f"{config['cmd']:<24} -> {config['modul']:<14} {waktu_ms:.2f} ms\n"
        self.text_command.insert(tk.END, pesan_log)
        self.text_command.see(tk.END)

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

        jumlah = 0
        try:
            with open('data/pesanan.csv', 'r') as file:
                header = file.readline()
                for baris in file:
                    elemen = baris.strip().split(',')
                    self.backend_array.append(elemen)
                    self.backend_ll.append(elemen)
                    jumlah += 1

            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(
                tk.END,
                f"DATA BERHASIL DIMUAT:\nTotal {jumlah:,} baris pesanan dari data/pesanan.csv telah dimuat ke Array dan Linked List.\n"
                f"Status: Siap diuji performanya."
            )

            # Format log COMMAND: load -> M1 - larik {waktu} ms
            pesan_log = f"{'load':<24} -> {'M1 - larik':<14} {waktu_ms:.2f} ms\n"
            self.text_command.insert(tk.END, pesan_log)
            self.text_command.see(tk.END)

        except FileNotFoundError:
            self.text_hasil.delete(1.0, tk.END)
            self.text_hasil.insert(tk.END, "Error: File data/pesanan.csv tidak ditemukan!")
            pesan_log = f"{'load':<24} -> {'M1 - larik':<14} GAGAL\n"
            self.text_command.insert(tk.END, pesan_log)
            self.text_command.see(tk.END)