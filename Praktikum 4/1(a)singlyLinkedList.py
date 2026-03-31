class Node:
    def __init__(self, digit):
        self.digit = digit
        self.next = None
class BigIntegerLL:
    def __init__(self, value="0"):
        self.head = None
        for digit in value:
            self.append(int(digit))
    def append(self, digit):
        new_node = Node(digit)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
    def toString(self):
        result = []
        temp = self.head
        while temp:
            result.append(str(temp.digit))
            temp = temp.next
        return ''.join(result)
    def add(self, other):
        s1 = self.toString()[::-1]
        s2 = other.toString()[::-1]
        carry = 0
        result = ""
        for i in range(max(len(s1), len(s2))):
            d1 = int(s1[i]) if i < len(s1) else 0
            d2 = int(s2[i]) if i < len(s2) else 0
            total = d1 + d2 + carry
            carry = total // 10
            result += str(total % 10)
        if carry:
            result += str(carry)
        return BigIntegerLL(result[::-1])


if __name__ == "__main__":
    print("=== Big Integer Linked List ===")
    angka1 = input("Masukkan angka pertama: ")
    angka2 = input("Masukkan angka kedua: ")
    a = BigIntegerLL(angka1)
    b = BigIntegerLL(angka2)
    hasil = a.add(b)
    print("Hasil:", hasil.toString())