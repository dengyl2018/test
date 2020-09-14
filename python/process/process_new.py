#coding=utf-8
from multiprocessing import Process
import time

class BaseProcess(Process):
    def __init__(self, desc, **attr):
        self.desc = desc
        if attr:
            self.__set_attr(**attr)
        Process.__init__(self)
    
    def __set_attr(self, **attr):
        for key, value in attr.items():
            if key in dir(self):
                continue
            setattr(self, key, value)
    
    def run(self):
        while True:
            time.sleep(1)
            print("hello")


class Process1(BaseProcess):
    def run(self):
        while True:
            time.sleep(1)
            print("process - 1")


class Process2(BaseProcess):
    def run(self):
        while True:
            time.sleep(1)
            print("process - 2")


def main():
    BaseProcess(
        "desc"
    ).start()
    Process1(
        "desc"
    ).start()
    Process2(
        "desc"
    ).start()


if __name__ == "__main__":
    main()