"""
https://www.cnblogs.com/AmilyWilly/p/8570318.html   
"""
#coding=utf-8
import threading
from threading import Thread
import time
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def count(x, y):

    c = 0
    while c < 5000000:
        c += 1
        x += x
        y += y

def write():
    f = open("test.txt", "w")
    for x in range(5000000):
        f.write("testwrite\n")
    f.close()
 
def read():
    f = open("test.txt", "r")
    lines = f.readlines()
    f.close()

_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
url = "http://www.tieba.com"
def http_request():
    try:
        import pdb; pdb.set_trace()
        webPage = requests.get(url, headers=_head)
        html = webPage.text
        return {"context": html}
    except Exception as e:
        return {"error": e}


class BaseThread(Thread):
    def __init__(self, desc, callback_func, **attr):
        super(BaseThread, self).__init__(name=desc)
        self.desc = desc
        self.callback_func = callback_func
        if attr:
            self.__set_attr(**attr)
        
    def __set_attr(self, **attr):
        for key, value in attr.items():
            if key in dir(self):
                continue
            setattr(self, key, value)
    
    def run(self):
        while True:
            print("hello")
            self.callback_func(self.desc)
            time.sleep(1)


class Thread1(BaseThread):
    def run(self):
        while True:
            print("thread - 1")
            self.callback_func(self.desc)
            time.sleep(1)


class Thread2(BaseThread):
    def run(self):
        while True:
            print("thread - 2")
            self.callback_func(self.desc)
            time.sleep(1)


def main():
    lock = threading.Lock()
    def callback_func(name):
        if lock.acquire():
            print("call back: %s" % name)
            lock.release()

    thread = BaseThread("test", callback_func)
    thread.setDaemon(True)
    thread.start()

    thread = Thread1("test - 1", callback_func)
    thread.setDaemon(True)
    thread.start()

    thread = Thread2("test - 2", callback_func)
    thread.setDaemon(True)
    thread.start()

    time.sleep(10)


if __name__ == "__main__":
    http_request()


    # main()
    # counts = []
    # t = time.time()
    # for x in range(10):
    #     thread = Thread(target=count, args=(1,1))
    #     counts.append(thread)
    #     thread.start()
    
    # e = counts.__len__()
    # while True:
    #     for th in counts:
    #         if not th.is_alive():
    #             e -= 1
    #     if e <= 0:
    #         break
    # print(time.time() - t)