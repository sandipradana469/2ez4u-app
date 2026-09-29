import tkinter as tk
from frontend.ui import AppUI
from backend.m1_pesanan import Array, LinkList
from backend.m2_antrean import QueueNaif, AntreanMelingkar, ManajerUndoRedo

if __name__ == "__main__":
    root = tk.Tk()

    # Struktur Data M1: Array Dinamis & Singly Linked List
    pesanan_array = Array()
    pesanan_ll = LinkList()

    # Struktur Data M2: Queue Naif, Antrean Melingkar, dan Manajer Undo/Redo
    queue_naif = QueueNaif()
    queue_circular = AntreanMelingkar()
    manajer_undo = ManajerUndoRedo()

    # Mengirim objek backend M1 & M2 ke Antarmuka Tkinter
    app = AppUI(
        root,
        pesanan_array,
        pesanan_ll,
        queue_naif=queue_naif,
        queue_circular=queue_circular,
        manajer_undo=manajer_undo
    )

    # Otomatis memuat data pesanan CSV saat startup
    app.aksi_load()

    root.mainloop()