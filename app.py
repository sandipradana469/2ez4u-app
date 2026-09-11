import tkinter as tk
from frontend.ui import AppUI
from backend.m1_pesanan import Array, LinkList

def baca_pesanan_csv():
    data_pesanan = []
    try:
        with open('data/pesanan.csv', 'r') as file:
            header = file.readline() 
            for baris in file:
                elemen = baris.strip().split(',')
                data_pesanan.append(elemen)
        return data_pesanan
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    print("Memuat data pesanan...")
    larik_data = baca_pesanan_csv()
    
    pesanan_array = Array()
    pesanan_ll = LinkList()
    
    for baris in larik_data:
        pesanan_array.append(baris)
        pesanan_ll.append(baris)
        
    print("Berhasil memuat data ke Array dan Linked List!")

    root = tk.Tk()
    # Mengirim kedua objek ke UI
    app = AppUI(root, pesanan_array, pesanan_ll)
    root.mainloop()