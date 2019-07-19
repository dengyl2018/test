# coding=utf-8
"""
有N个人排成一排，从1到N按顺序依次编号，现在要执行N次操作，
第一次操作让所有的人都蹲下，之后第二次操作让编号是2和2的倍数的人全部站起来，
然后第三次操作让编号是3和3的倍数的人全部做相反的动作（站着的人蹲下，蹲下的人站起来），
以此类推...，最后第N次操作让编号为N的这个人也做相反的动作。
请问N次操作后，从第A个人到第B个人之间（包括A和B这两个数字,且A<B）有多少人是站着的？
"""

import pdb
import datetime

class StandUp(object):
    """
    standUp
    """
    def __init__(self, n, a, b):
        """
        init
        蹲下：0
        站起：1
        a:0 ~ n-1
        b:0 ~ n-1
        """
        self.n = n
        self.a = a
        self.b = b
        self.list_n = [0 for i in range(0, n)]

    def run(self):
        """
        run
        """
        t_before = datetime.datetime.now()
        if not (self.a >= 0 and self.b >= self.a and self.n > self.b):
            return "a=%s, b=%s, n=%s" % (self.a, self.b, self.n)
        self.update_list_n()
        sum = 0
        for i in range(self.a, self.b):
            sum += self.list_n[i]
        print "cost: %s (us)" % (datetime.datetime.now() - t_before).microseconds
        return sum

    def update_list_n(self):
        """
        update
        """
        for i in range(2, self.n + 1): # 调整的次数 2-n 次
            for j in range(0, self.n): # 遍历数组
                if (j + 1) % i == 0:
                    self.list_n[j] = self._change_status(self.list_n[j])
    
    def _change_status(self, status):
        """
        0 -> 1
        1 -> 0
        """
        return 1 if status == 0 else 0





    