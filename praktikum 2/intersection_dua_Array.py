def intersection():
    arr1 = input("masukkan array pertama : ").split()
    arr2 = input("masukkan array kedua : ").split()
    hasil = list(set(arr1) & set(arr2))
    print("intersection:", hasil)

if __name__ == "__main__":
    intersection()