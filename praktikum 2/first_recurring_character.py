def first_recurring():
    s = input("masukkan sebuah string: ")
    seen = set()
    for char in s:
        if char in seen:
            print("karakter berulang pertama:", char)
            return
        seen.add(char)
    print("tidak ada karakter berulang")

if __name__ == "__main__":
    first_recurring()