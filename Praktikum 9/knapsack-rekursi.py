def knapsack(weights, target, index, current):
    if target == 0:
        print("Solusi ditemukan:", current)
        return True

    if target < 0 or index == len(weights):
        return False


    if knapsack(
        weights,
        target - weights[index],
        index + 1,
        current + [weights[index]]
    ):
        return True

    
    return knapsack(
        weights,
        target,
        index + 1,
        current
    )


weights = [2, 5, 6, 9, 12, 14, 20]

target = int(input("Masukkan berat target (2,5,6,9,12,14,20): "))

if not knapsack(weights, target, 0, []):
    print("Tidak ada kombinasi.")