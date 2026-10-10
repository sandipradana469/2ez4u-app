
# kolom csv
IDX_OID = 0
IDX_HARGA = 4
IDX_SELESAI = 7

# ambil nilai pembanding
def normalisasi_kunci(kunci):
    teks = (kunci or "").strip().lower()
    if teks == "oid":
        return "oid"
    if teks == "harga":
        return "harga"
    if teks == "selesai" or teks == "t_selesai" or teks == "t_selesai_detik":
        return "selesai"
    return None

def ambil_kunci(pesanan, kunci):
    if pesanan is None:
        return ""

    if kunci == "harga":
        return _ke_int(pesanan, IDX_HARGA, 0)
    if kunci == "selesai":
        nilai = _ambil_kolom(pesanan, IDX_SELESAI)
        if nilai == "":
            return 999999999
        return _ke_int(pesanan, IDX_SELESAI, 999999999)
    return _ambil_kolom(pesanan, IDX_OID)

def _ambil_kolom(pesanan, indeks):
    if indeks < len(pesanan):
        return pesanan[indeks].strip()
    return ""

def _ke_int(pesanan, indeks, default):
    teks = _ambil_kolom(pesanan, indeks)
    if teks == "":
        return default
    try:
        return int(teks)
    except ValueError:
        return default

def bandingkan(a, b, kunci):
    ka = ambil_kunci(a, kunci)
    kb = ambil_kunci(b, kunci)
    if ka < kb:
        return -1
    if ka > kb:
        return 1
    return 0

def salin_data(larik, jumlah):
    n = jumlah
    if n < 0:
        n = 0
    if n > len(larik):
        n = len(larik)

    hasil = [None] * n
    for i in range(n):
        hasil[i] = larik[i]
    return hasil

# sorting
def insertion_sort(larik, kunci):
    data = salin_data(larik, len(larik))
    perbandingan = 0
    pemindahan = 0

    for i in range(1, len(data)):
        item = data[i]
        j = i - 1

        while j >= 0:
            perbandingan += 1
            if bandingkan(data[j], item, kunci) <= 0:
                break
            data[j + 1] = data[j]
            pemindahan += 1
            j -= 1

        data[j + 1] = item
        pemindahan += 1

    return data, perbandingan, pemindahan

def merge_sort(larik, kunci):
    data = salin_data(larik, len(larik))
    bantu = [None] * len(data)
    metrik = [0, 0]
    _merge_sort_rekursif(data, bantu, 0, len(data), kunci, metrik)
    return data, metrik[0], metrik[1]

def _merge_sort_rekursif(data, bantu, kiri, kanan, kunci, metrik):
    if kanan - kiri <= 1:
        return

    tengah = (kiri + kanan) // 2
    _merge_sort_rekursif(data, bantu, kiri, tengah, kunci, metrik)
    _merge_sort_rekursif(data, bantu, tengah, kanan, kunci, metrik)
    _gabung(data, bantu, kiri, tengah, kanan, kunci, metrik)

def _gabung(data, bantu, kiri, tengah, kanan, kunci, metrik):
    i = kiri
    j = tengah
    k = kiri

    while i < tengah and j < kanan:
        metrik[0] += 1
        if bandingkan(data[i], data[j], kunci) <= 0:
            bantu[k] = data[i]
            i += 1
        else:
            bantu[k] = data[j]
            j += 1
        metrik[1] += 1
        k += 1

    while i < tengah:
        bantu[k] = data[i]
        metrik[1] += 1
        i += 1
        k += 1

    while j < kanan:
        bantu[k] = data[j]
        metrik[1] += 1
        j += 1
        k += 1

    for p in range(kiri, kanan):
        data[p] = bantu[p]
        metrik[1] += 1

# searching
def linear_search(larik, target_oid):
    target = (target_oid or "").strip()
    perbandingan = 0

    for i in range(len(larik)):
        perbandingan += 1
        if _ambil_kolom(larik[i], IDX_OID) == target:
            return i, larik[i], perbandingan

    return -1, None, perbandingan

def binary_search(larik_terurut_oid, target_oid):
    target = (target_oid or "").strip()
    kiri = 0
    kanan = len(larik_terurut_oid) - 1
    perbandingan = 0

    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        oid = _ambil_kolom(larik_terurut_oid[tengah], IDX_OID)
        perbandingan += 1

        if oid == target:
            return tengah, larik_terurut_oid[tengah], perbandingan
        if oid < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1

    return -1, None, perbandingan




