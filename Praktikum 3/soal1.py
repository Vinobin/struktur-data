def findLeft(arr, target):
    low = 0
    high = len(arr) - 1
    result = -1
    
    while low <= high:
        mid = (low + high) // 2
        
        if arr[mid] == target:
            result = mid
            high = mid - 1
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return result


def findRight(arr, target):
    low = 0
    high = len(arr) - 1
    result = -1
    
    while low <= high:
        mid = (low + high) // 2
        
        if arr[mid] == target:
            result = mid
            low = mid + 1
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return result


def countOccurrences(sortedList, target):
    left = findLeft(sortedList, target)
    
    if left == -1:
        return 0
    
    right = findRight(sortedList, target)
    
    return right - left + 1


print(countOccurrences([1,2,4,4,4,7,9,12],4))
print(countOccurrences([1,2,4,4,4,7,9,12],5))