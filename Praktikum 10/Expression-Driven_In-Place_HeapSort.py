from typing import List, Optional
from collections import deque


class ExprNode:

    def __init__(self, val):

        self.val = val
        self.left = None
        self.right = None


class ExprHeapSorter:

    def __init__(self, expr_str: str):

        self.expr = expr_str
        self.values = []

    # =====================================================
    # 1. BUILD & EVALUATE EXPRESSION TREE
    # =====================================================

    def parse_and_evaluate(self) -> List[int]:

        tokens = deque(self.expr)

        root = self._build_tree(tokens)

        self.values = self._eval_tree(root)

        return self.values

    def _build_tree(
            self,
            tokens: deque
    ) -> Optional[ExprNode]:

        if not tokens:
            return None

        token = tokens.popleft()

        # subtree baru
        if token == '(':

            left = self._build_tree(tokens)

            op = tokens.popleft()

            right = self._build_tree(tokens)

            # abaikan ')'
            tokens.popleft()

            node = ExprNode(op)

            node.left = left
            node.right = right

            return node

        # operand
        elif token.isdigit():

            return ExprNode(int(token))

        else:
            raise ValueError("Token tidak valid")

    def _eval_tree(
            self,
            node: Optional[ExprNode]
    ) -> List[int]:

        if node is None:
            return []

        # leaf node
        if node.left is None and node.right is None:
            return [node.val]

        left_vals = self._eval_tree(node.left)
        right_vals = self._eval_tree(node.right)

        a = left_vals[-1]
        b = right_vals[-1]

        op = node.val

        if op == '+':
            result = a + b

        elif op == '-':
            result = a - b

        elif op == '*':
            result = a * b

        elif op == '/':

            if b == 0:
                raise ValueError("Division by zero")

            result = a // b

        else:
            raise ValueError("Operator tidak valid")

        return left_vals + right_vals + [result]

    # =====================================================
    # 2. IN-PLACE HEAPSORT
    # =====================================================

    def heapsort_inplace(
            self,
            arr: List[int]
    ) -> List[int]:

        n = len(arr)

        if n <= 1:
            return arr

        # ==============================================
        # BUILD MAX HEAP
        # range(n//2 - 1, -1, -1)
        # ==============================================

        for i in range(n // 2 - 1, -1, -1):

            self._sift_down(arr, n, i)

        # ==============================================
        # SORTING
        # ==============================================

        for end in range(n - 1, 0, -1):

            # swap root dengan elemen akhir
            arr[0], arr[end] = arr[end], arr[0]

            # heap size berkurang
            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(
            self,
            arr: List[int],
            heap_size: int,
            idx: int):

        while True:

            largest = idx

            left = 2 * idx + 1
            right = 2 * idx + 2

            # bandingkan child kiri
            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            # bandingkan child kanan
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            # posisi valid
            if largest == idx:
                break

            # swap
            arr[idx], arr[largest] = arr[largest], arr[idx]

            # update index
            idx = largest

    # =====================================================
    # 3. COMPLETE TREE VALIDATION
    # =====================================================

    def is_complete_tree(
            self,
            arr: List[int]
    ) -> bool:

        n = len(arr)

        for i in range(n):

            left = 2 * i + 1
            right = 2 * i + 2

            # tidak boleh ada right child
            # tanpa left child
            if left >= n and right < n:
                return False

        return True


# =========================================================
# TESTING PROGRAM
# =========================================================

if __name__ == "__main__":

    expr = "((8*5)+(9/(7-4)))"

    sorter = ExprHeapSorter(expr)

    print("===== EXPRESSION TREE =====")

    values = sorter.parse_and_evaluate()

    print("Hasil evaluasi traversal:")
    print(values)

    print()

    print("===== HEAPSORT IN-PLACE =====")

    data = [40, 12, 90, 1, 55, 23, 8]

    print("Sebelum sorting:")
    print(data)

    sorter.heapsort_inplace(data)

    print("Sesudah sorting:")
    print(data)

    print()

    print("===== COMPLETE TREE CHECK =====")

    result = sorter.is_complete_tree(data)

    print("Apakah complete binary tree?")
    print(result)