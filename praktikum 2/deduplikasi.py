def deduplikasi():
    data = input("masukkan angka : ").split()
    hasil = []
    seen = set()
    for item in data:
        if item not in seen:
            seen.add(item)
            hasil.append(item)
    print("hasil tanpa duplikat:", hasil)

if __name__ == "__main__":
    deduplikasi()