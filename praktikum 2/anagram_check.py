def anagram():
    str1 =input("masukkan string pertama :")
    str2 =input("masukkan string kedua :")
    if len(str1) != len(str2):
        print("Bukan anagram")
        return
    count = {}
    for char in str1:
        count[char] = count.get(char, 0) + 1
    for char in str2:
        if char not in count:
            print("bukan anagram")
            return
        count[char] -= 1
        if count[char] < 0:
            print("bukan anagram")
            return
    print("adalah anagram ")

if __name__ == "__main__":
    anagram()