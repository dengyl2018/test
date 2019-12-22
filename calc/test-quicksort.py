#coding=utf-8

def quicksort(list0):
    """
    """
    if len(list0) <= 1:
        return list0
    mid = list0[0]
    list0.remove(mid)
    left, right = [], []
    for data in list0:
        if data >= mid:
            right.append(data)
        else:
            left.append(data)
    print "---"
    print mid
    print left + [mid] + right
    return quicksort(left) + [mid] + quicksort(right) 

if __name__ == "__main__":
    print quicksort([5, 3, 7, 6, 4, 1, 0, 2, 9, 10, 8])