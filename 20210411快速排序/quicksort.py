#coding=utf-8
"""
快速排序
"""

def qsort(data):
    """
    """
    if not isinstance(data, list) or len(data) <= 1:
        return data
    return qsort([i for i in data[1:] if i < data[0]]) + [data[0]] + qsort([i for i in data[1:] if i > data[0]])

data = [6, 1, 2, 7, 9, 3, 4, 5, 10, 8]
print(qsort(data))