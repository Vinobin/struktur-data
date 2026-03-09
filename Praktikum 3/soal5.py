#a
def countInversionsNaive(arr):
    count = 0

    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                count += 1

    return count

data = [8, 4, 2, 1]

print("Jumlah inversion (Naive):", countInversionsNaive(data))

#b
def merge(arr, temp, left, mid, right):

    i = left
    j = mid
    k = left
    inv_count = 0

    while i <= mid - 1 and j <= right:

        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1

            inv_count += (mid - i)

        k += 1

    while i <= mid - 1:
        temp[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1

    for i in range(left, right + 1):
        arr[i] = temp[i]

    return inv_count


def mergeSort(arr, temp, left, right):

    inv_count = 0

    if right > left:

        mid = (left + right) // 2

        inv_count += mergeSort(arr, temp, left, mid)
        inv_count += mergeSort(arr, temp, mid + 1, right)

        inv_count += merge(arr, temp, left, mid + 1, right)

    return inv_count


def countInversionsSmart(arr):

    temp = [0] * len(arr)
    return mergeSort(arr, temp, 0, len(arr) - 1)

data = [8, 4, 2, 1]

print("Jumlah inversion (Merge Sort):", countInversionsSmart(data))