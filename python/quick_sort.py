#coding=utf-8

def quick_sort1(q):
    if len(q) <= 1:
        return q
    left, right = [], []
    for i in range(len(q)):
        if i == len(q) / 2: continue
        if q[i] <= q[len(q) / 2]:
            left.append(q[i])
        else:
            right.append(q[i])
    return quick_sort1(left) + [q[len(q) / 2]] + quick_sort1(right)


quick_sort2 = lambda array: array if len(array) <= 1 \
        else quick_sort2([item for item in array[1:] if item <= array[0]]) \
            + [array[0]] \
            + quick_sort2([item for item in array[1:] if item > array[0]])
    

if __name__ == "__main__":
    q = [10, 3, 4, 5, 6, 4, 2, 7, -1]
    print(q)
    print(quick_sort1(q))
    print(q)
    print(quick_sort2(q))

