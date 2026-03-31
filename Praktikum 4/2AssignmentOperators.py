class BigIntegerList:
    def __init__(self, value="0"):
        self.value = int(value)
    def __iadd__(self, other):
        self.value += other.value
        return self
    def __isub__(self, other):
        self.value -= other.value
        return self
    def __imul__(self, other):
        self.value *= other.value
        return self
    def __ifloordiv__(self, other):
        self.value //= other.value
        return self
    def __imod__(self, other):
        self.value %= other.value
        return self
    def __str__(self):
        return str(self.value)



if __name__ == "__main__":
    print("=== Big Integer Operator ===")
    angka1 = input("Masukkan angka pertama: ")
    angka2 = input("Masukkan angka kedua: ")
    op = input("Pilih operator (+, -, *, //, %): ")
    a = BigIntegerList(angka1)
    b = BigIntegerList(angka2)
    if op == "+":
        a += b
    elif op == "-":
        a -= b
    elif op == "*":
        a *= b
    elif op == "//":
        a //= b
    elif op == "%":
        a %= b
    else:
        print("Operator tidak valid")
    print("Hasil:", a)