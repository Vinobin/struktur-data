class BigIntegerList:
    def __init__(self, value="0"):
        self.digits = [int(d) for d in reversed(value)]
    def toString(self):
        return ''.join(map(str, reversed(self.digits)))
    def add(self, other):
        result = []
        carry = 0
        for i in range(max(len(self.digits), len(other.digits))):
            d1 = self.digits[i] if i < len(self.digits) else 0
            d2 = other.digits[i] if i < len(other.digits) else 0
            total = d1 + d2 + carry
            carry = total // 10
            result.append(total % 10)
        if carry:
            result.append(carry)
        res = BigIntegerList("0")
        res.digits = result
        return res



if __name__ == "__main__":
    print("=== Big Integer List ===")
    angka1 = input("Masukkan angka pertama: ")
    angka2 = input("Masukkan angka kedua: ")
    a = BigIntegerList(angka1)
    b = BigIntegerList(angka2)
    hasil = a.add(b)
    print("Hasil:", hasil.toString())