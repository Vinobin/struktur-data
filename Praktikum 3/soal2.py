def bubbleSort(arr):
    n = len(arr)
    comparisons = 0
    swaps = 0
    passes = 0
    
    for i in range(n-1):
        swapped = False
        passes += 1
        
        for j in range(n-i-1):
            comparisons += 1
            
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
                swapped = True
        
        print("Pass", passes, ":", arr)
        
        if not swapped:
            break
    
    return arr, comparisons, swaps, passes


print(bubbleSort([5,1,4,2,8]))
print(bubbleSort([1,2,3,4,5]))