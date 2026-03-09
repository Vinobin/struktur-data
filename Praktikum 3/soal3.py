def insertionSort(arr):
    comparisons = 0
    swaps = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            j -= 1
            swaps += 1

        arr[j + 1] = key

    return comparisons + swaps


def selectionSort(arr):
    ops = 0
    n = len(arr)

    for i in range(n - 1):
        min_idx = i

        for j in range(i + 1, n):
            ops += 1
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return ops


def hybridSort(arr, threshold=10):

    if len(arr) <= threshold:
        print("Menggunakan Insertion Sort")
        operations = insertionSort(arr)
    else:
        print("Menggunakan Selection Sort")
        operations = selectionSort(arr)

    return arr, operations

data = [9, 3, 7, 1, 5, 2]

sorted_data, ops = hybridSort(data)

print("Hasil sorting:", sorted_data)
print("Jumlah operasi:", ops)