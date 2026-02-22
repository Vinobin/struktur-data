def buku_telepon():
    kontak = {}
    while True:
        print("\n=== MENU BUKU TELEPON ===")
        print("1. Tambah kontak")
        print("2. Cari kontak")
        print("3. Tampilkan semua")
        print("4. Kembali ke menu utama")
        pilihan = input("pilih menu: ")
        if pilihan == "1":
            nama = input("Masukkan nama: ")
            nomor = input("Masukkan nomor: ")
            kontak[nama] = nomor
            print("Kontak berhasil ditambahkan!")
        elif pilihan == "2":
            nama = input("Masukkan nama yang dicari: ")
            if nama in kontak:
                print(f"Nomor {nama}: {kontak[nama]}")
            else:
                print("Kontak tidak ditemukan.")
        elif pilihan == "3":
            if not kontak:
                print("Belum ada kontak.")
            else:
                for nama, nomor in kontak.items():
                    print(f"{nama} : {nomor}")
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid!")
if __name__ == "__main__":
    buku_telepon()