from typing import List, Optional
import math


class ListNode:

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class AdvancedSorter:

    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT
    # Virtual Sublists + Single tmpArray
    # =========================================================

    def sort_array(self, arr: List[int]) -> List[int]:

        if len(arr) <= 1:
            return arr

        # hanya satu tmpArray
        tmp_array = [0] * len(arr)

        self._rec_merge_sort(
            arr,
            0,
            len(arr) - 1,
            tmp_array
        )

        return arr

    def _rec_merge_sort(
            self,
            arr,
            first,
            last,
            tmp_array):

        if first >= last:
            return

        mid = (first + last) // 2

        self._rec_merge_sort(
            arr,
            first,
            mid,
            tmp_array
        )

        self._rec_merge_sort(
            arr,
            mid + 1,
            last,
            tmp_array
        )

        self._merge_virtual(
            arr,
            first,
            mid,
            last,
            tmp_array
        )

    def _merge_virtual(
            self,
            arr,
            left_start,
            mid,
            right_end,
            tmp_array):

        left = left_start
        right = mid + 1
        idx = left_start

        # STABLE
        while left <= mid and right <= right_end:

            # gunakan <= agar stabil
            if arr[left] <= arr[right]:

                tmp_array[idx] = arr[left]
                left += 1

            else:

                tmp_array[idx] = arr[right]
                right += 1

            idx += 1

        while left <= mid:

            tmp_array[idx] = arr[left]

            left += 1
            idx += 1

        while right <= right_end:

            tmp_array[idx] = arr[right]

            right += 1
            idx += 1

        # copy kembali ke array asli
        for i in range(left_start, right_end + 1):
            arr[i] = tmp_array[i]

    # =========================================================
    # 2. LINKED LIST MERGE SORT
    # Fast-Slow Pointer + Dummy Merge
    # =========================================================

    def sort_linked_list(
            self,
            head: Optional[ListNode]
    ) -> Optional[ListNode]:

        if head is None or head.next is None:
            return head

        # split linked list
        right_head = self._split_linked_list(head)

        left_head = head

        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        return self._merge_linked_lists(
            left_sorted,
            right_sorted
        )

    def _split_linked_list(
            self,
            head: ListNode
    ) -> Optional[ListNode]:

        # fast-slow pointer
        midPoint = head
        curNode = head.next

        while curNode and curNode.next:

            midPoint = midPoint.next
            curNode = curNode.next.next

        right_head = midPoint.next

        # putus linked list
        midPoint.next = None

        return right_head

    def _merge_linked_lists(
            self,
            listA: Optional[ListNode],
            listB: Optional[ListNode]
    ) -> Optional[ListNode]:

        # dummy node
        dummy = ListNode(0)

        tail = dummy

        while listA and listB:

            # STABLE
            if listA.data <= listB.data:

                tail.next = listA
                listA = listA.next

            else:

                tail.next = listB
                listB = listB.next

            tail = tail.next

        # sisa node
        tail.next = listA if listA else listB

        return dummy.next

    # =========================================================
    # 3. QUICK SORT
    # Median-of-Three + Depth Limiter
    # =========================================================

    def quick_sort(self, arr: List[int]) -> List[int]:

        if len(arr) <= 1:
            return arr

        self.quick_sort_recursive(
            arr,
            0,
            len(arr) - 1,
            0
        )

        return arr

    def quick_sort_recursive(
            self,
            arr,
            first,
            last,
            depth=0):

        if first >= last:
            return

        n = last - first + 1

        # depth limiter
        if n > 0 and depth > 2 * math.log2(n):

            # fallback ke merge sort
            temp = []

            for i in range(first, last + 1):
                temp.append(arr[i])

            self.sort_array(temp)

            for i in range(len(temp)):
                arr[first + i] = temp[i]

            return

        split_point = self.partition_quick(
            arr,
            first,
            last
        )

        self.quick_sort_recursive(
            arr,
            first,
            split_point - 1,
            depth + 1
        )

        self.quick_sort_recursive(
            arr,
            split_point + 1,
            last,
            depth + 1
        )

    def partition_quick(
            self,
            arr: List[int],
            first: int,
            last: int
    ) -> int:

        mid = (first + last) // 2

        # median-of-three
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]

        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]

        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]

        # median dipindah ke depan
        arr[first], arr[mid] = arr[mid], arr[first]

        pivot = arr[first]

        left = first + 1
        right = last

        done = False

        while not done:

            while left <= right and arr[left] <= pivot:
                left += 1

            while right >= left and arr[right] >= pivot:
                right -= 1

            if right < left:
                done = True

            else:
                arr[left], arr[right] = arr[right], arr[left]

        # tempatkan pivot
        arr[first], arr[right] = arr[right], arr[first]

        return right


# =========================================================
# TESTING PROGRAM
# =========================================================

if __name__ == "__main__":

    sorter = AdvancedSorter()

    # =====================================================
    # TEST MERGE SORT ARRAY
    # =====================================================

    arr1 = [38, 27, 43, 3, 9, 82, 10]

    print("===== MERGE SORT ARRAY =====")
    print("Sebelum Sorting:")
    print(arr1)

    sorter.sort_array(arr1)

    print("Sesudah Sorting:")
    print(arr1)

    print()

    # =====================================================
    # TEST QUICK SORT
    # =====================================================

    arr2 = [45, 12, 9, 30, 1, 100]

    print("===== QUICK SORT =====")
    print("Sebelum Sorting:")
    print(arr2)

    sorter.quick_sort(arr2)

    print("Sesudah Sorting:")
    print(arr2)

    print()

    # =====================================================
    # TEST LINKED LIST MERGE SORT
    # =====================================================

    head = ListNode(40)
    head.next = ListNode(10)
    head.next.next = ListNode(70)
    head.next.next.next = ListNode(20)

    print("===== LINKED LIST MERGE SORT =====")

    print("Sebelum Sorting:")

    cur = head

    while cur:
        print(cur.data, end=" -> ")
        cur = cur.next

    print("None")

    sorted_head = sorter.sort_linked_list(head)

    print("Sesudah Sorting:")

    cur = sorted_head

    while cur:
        print(cur.data, end=" -> ")
        cur = cur.next

    print("None")