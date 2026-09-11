import tkinter as tk
from tkinter import simpledialog
import time

class AppUI:
    def __init__(self, root, backend_array, backend_ll):
        self.root = root
        self.backend_array = backend_array
        self.backend_ll = backend_ll
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1000x600")

        # ================================================================
        # STRUKTUR LAYOUT:
        #   root
        #   ├── frame_kiri  (LEFT, fill=Y)        ← panel tombol, full tinggi
        #   └── frame_kanan (LEFT, fill=BOTH)     ← panel kanan
        #       ├── label + form                  (TOP)
        #       ├── frame_bawah / COMMAND         (BOTTOM) ← harus pack BOTTOM dulu
        #       └── frame_hasil / output          (fill=BOTH, expand) ← sisa ruang
        # ================================================================

        # --- PANEL KIRI (MENU NAVIGASI) ---
        self.frame_kiri = tk.Frame(root, bg="#e0e0e0", relief=tk.RIDGE, bd=1)
        self.frame_kiri.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.frame_kiri, text="M1 - DATA PESANAN", bg="#e0e0e0",
                 font=("Arial", 9, "bold")).pack(anchor="w", padx=5, pady=(8, 2))
        tk.Button(self.frame_kiri, text="ARRAY - LIHAT PESANAN", anchor="w",
                  command=lambda: self.test_lihat("ARRAY")).pack(fill=tk.X, padx=5, pady=1)
        tk.Button(self.frame_kiri, text="ARRAY - TAMBAH PESANAN REGULER", anchor="w",
                  command=lambda: self.test_tambah("ARRAY", "REGULER")).pack(fill=tk.X, padx=5, pady=1)
        tk.Button(self.frame_kiri, text="ARRAY - TAMBAH PESANAN PRIORITAS", anchor="w",
                  command=lambda: self.test_tambah("ARRAY", "PRIORITAS")).pack(fill=tk.X, padx=5, pady=1)
        tk.Button(self.frame_kiri, text="ARRAY - TAMBAH PESANAN VIP", anchor="w",
                  command=lambda: self.test_tambah("ARRAY", "VIP")).pack(fill=tk.X, padx=5, pady=1)
        tk.Button(self.frame_kiri, text="ARRAY - HAPUS PESANAN", anchor="w",
                  command=lambda: self.test_hapus("ARRAY")).pack(fill=tk.X, padx=5, pady=1)

        tk.Button(self.frame_kiri, text="LINKLIST - LIHAT PESANAN", anchor="w",
                  command=lambda: self.test_lihat("LINKLIST")).pack(fill=tk.X, padx=5, pady=1)
        tk.Button(self.frame_kiri, text="LINKLIST - TAMBAH PESANAN REGULER", anchor="w",
                  command=lambda: self.test_tambah("LINKLIST", "REGULER")).pack(fill=tk.X, padx=5, pady=1)
        tk.Button(self.frame_kiri, text="LINKLIST - TAMBAH PESANAN PRIORITAS", anchor="w",
                  command=lambda: self.test_tambah("LINKLIST", "PRIORITAS")).pack(fill=tk.X, padx=5, pady=1)
        tk.Button(self.frame_kiri, text="LINKLIST - TAMBAH PESANAN VIP", anchor="w",
                  command=lambda: self.test_tambah("LINKLIST", "VIP")).pack(fill=tk.X, padx=5, pady=1)
        tk.Button(self.frame_kiri, text="LINKLIST - HAPUS PESANAN", anchor="w",
                  command=lambda: self.test_hapus("LINKLIST")).pack(fill=tk.X, padx=5, pady=1)

        # --- PANEL KANAN ---
        self.frame_kanan = tk.Frame(root, bg="white")
        self.frame_kanan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Tambah Pesanan (TOP)
        tk.Label(self.frame_kanan, text="Form Tambah Pesanan", bg="white",
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 4))

        self.frame_form = tk.Frame(self.frame_kanan, bg="white")
        self.frame_form.pack(fill=tk.X, padx=20)

        self.var_nama  = tk.StringVar(value="Pelanggan Baru")
        self.var_resto = tk.StringVar(value="Mie Gacoan")
        self.var_menu  = tk.StringVar(value="Mie Hompimpa Level 2, Udang Keju")
        self.var_harga = tk.StringVar(value="15000")

        fields = [
            ("Nama pelanggan:", self.var_nama),
            ("Restoran:",       self.var_resto),
            ("Menu dipesan:",   self.var_menu),
            ("Harga (Rp):",     self.var_harga),
        ]
        for i, (label_text, var) in enumerate(fields):
            tk.Label(self.frame_form, text=label_text, bg="white",
                     font=("Arial", 10)).grid(row=i, column=0, sticky="w", pady=2)
            tk.Entry(self.frame_form, textvariable=var, width=40
                     ).grid(row=i, column=1, padx=10, pady=2)

        # COMMAND LOG (BOTTOM) — harus di-pack sebelum text_hasil agar tidak terpotong
        self.frame_bawah = tk.Frame(self.frame_kanan, height=120, bg="white", relief=tk.RIDGE, bd=1)
        self.frame_bawah.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        self.frame_bawah.pack_propagate(False)

        tk.Label(self.frame_bawah, text="COMMAND", bg="white",
                 font=("Arial", 9, "bold")).pack(anchor="w", padx=5, pady=(3, 0))

        frame_log_inner = tk.Frame(self.frame_bawah, bg="white")
        frame_log_inner.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        scroll_log = tk.Scrollbar(frame_log_inner)
        self.text_command = tk.Text(
            frame_log_inner,
            fg="black", bg="white",
            font=("Consolas", 10),
            yscrollcommand=scroll_log.set
        )
        scroll_log.config(command=self.text_command.yview)
        scroll_log.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_command.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_command.insert(tk.END, "Sistem 2EZ4U siap berjalan...\n")

        # OUTPUT HASIL (mengisi sisa ruang di tengah)
        tk.Label(self.frame_kanan, text="", bg="white").pack()  # spacer kecil

        frame_hasil_wrap = tk.Frame(self.frame_kanan, bg="white")
        frame_hasil_wrap.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 5))

        scroll_hasil = tk.Scrollbar(frame_hasil_wrap)
        self.text_hasil = tk.Text(
            frame_hasil_wrap,
            font=("Arial", 10),
            yscrollcommand=scroll_hasil.set
        )
        scroll_hasil.config(command=self.text_hasil.yview)
        scroll_hasil.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_hasil.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_hasil.insert(tk.END, "Tekan tombol di panel kiri untuk melihat hasil di sini...")

    # =====================================================================
    # FUNGSI BACKEND M1
    # =====================================================================

    def test_tambah(self, struktur, prioritas):
        nama  = self.var_nama.get()
        resto = self.var_resto.get()
        menu  = self.var_menu.get()
        harga = self.var_harga.get()

        target_ds = self.backend_array if struktur == "ARRAY" else self.backend_ll
        oid_baru = f"0-{200000 + target_ds.ukuran + 1}"
        pesanan_baru = [oid_baru, nama, resto, menu, harga, "3", "45000", "", "ANTRE"]

        mulai = time.perf_counter()

        if prioritas == "REGULER":
            target_ds.append(pesanan_baru)
        elif prioritas == "PRIORITAS":
            indeks_tengah = target_ds.ukuran // 2
            target_ds.insert(indeks_tengah, pesanan_baru)
        elif prioritas == "VIP":
            target_ds.insert(0, pesanan_baru)

        selesai  = time.perf_counter()
        waktu_ms = (selesai - mulai) * 1000

        if prioritas == "REGULER":
            keterangan = "masuk di posisi paling BELAKANG (antrian normal)"
        elif prioritas == "PRIORITAS":
            keterangan = "masuk di posisi TENGAH antrian"
        else:  # VIP
            keterangan = "masuk di posisi paling DEPAN antrian"

        self.text_hasil.delete(1.0, tk.END)
        self.text_hasil.insert(tk.END,
            f"[{struktur}] Tambah pesanan {prioritas}\n"
            f"  → {keterangan}\n\n"
            f"Data pesanan yang ditambahkan:\n{pesanan_baru}"
        )

        pesan_log = f"[{struktur}] OID {oid_baru} masuk ({prioritas}) | Waktu: {waktu_ms:.4f} ms\n"
        self.text_command.insert(tk.END, pesan_log)
        self.text_command.see(tk.END)

    def test_lihat(self, struktur):
        indeks = simpledialog.askinteger(
            "Input Indeks",
            f"Masukkan indeks pesanan untuk dilihat di {struktur}:",
            minvalue=0
        )
        if indeks is not None:
            target_ds = self.backend_array if struktur == "ARRAY" else self.backend_ll

            mulai   = time.perf_counter()
            hasil   = target_ds.get(indeks)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            if hasil is not None:
                pesan_log = f"[{struktur}] LIHAT indeks {indeks} | Waktu: {waktu_ms:.4f} ms\n"
                self.text_hasil.delete(1.0, tk.END)
                self.text_hasil.insert(tk.END, f"DATA DITEMUKAN PADA INDEKS {indeks}:\n{hasil}")
            else:
                pesan_log = f"[{struktur}] LIHAT indeks {indeks} GAGAL | Waktu: {waktu_ms:.4f} ms\n"
                self.text_hasil.delete(1.0, tk.END)
                self.text_hasil.insert(tk.END, "DATA TIDAK DITEMUKAN / INDEKS DI LUAR BATAS")

            self.text_command.insert(tk.END, pesan_log)
            self.text_command.see(tk.END)

    def test_hapus(self, struktur):
        indeks = simpledialog.askinteger(
            "Input Indeks",
            f"Masukkan indeks pesanan yang akan dihapus dari {struktur}:",
            minvalue=0
        )
        if indeks is not None:
            target_ds = self.backend_array if struktur == "ARRAY" else self.backend_ll

            mulai   = time.perf_counter()
            dihapus = target_ds.hapus(indeks)
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000

            if dihapus is not None:
                pesan_log = f"[{struktur}] HAPUS indeks {indeks} | Waktu: {waktu_ms:.4f} ms\n"
                self.text_hasil.delete(1.0, tk.END)
                self.text_hasil.insert(tk.END, f"DATA BERHASIL DIHAPUS:\n{dihapus}")
            else:
                pesan_log = f"[{struktur}] HAPUS indeks {indeks} GAGAL | Waktu: {waktu_ms:.4f} ms\n"
                self.text_hasil.delete(1.0, tk.END)
                self.text_hasil.insert(tk.END, "GAGAL MENGHAPUS / INDEKS DI LUAR BATAS")

            self.text_command.insert(tk.END, pesan_log)
            self.text_command.see(tk.END)