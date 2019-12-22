#coding=utf-8
"""
多线程
"""
import re
import time
import requests
from queue import Queue
import threading
from threading import Thread
from bs4 import BeautifulSoup
from lxml import etree
import multiprocessing

HEADERS = {
        'Accept': '',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': '',
        'DNT': '1',
        'Host': 'www.g.com',
        'Referer': '',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

def run(in_q, out_q):
    """
    多线程
    """
    headers = HEADERS
    while not in_q.empty():
        data = requests.get(url=in_q.get(), headers=headers)
        r = data.content
        content = str(r, encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(content, "html5lib")
        fixed_html = soup.prettify()
        html = etree.HTML(fixed_html)
        nums = html.xpath('//div[@class="col-md-1"]//text()')
        for num in nums:
            num = re.findall('[0-9]', ''.join(num))
            real_num = int(''.join(num))
            out_q.put(str(threading.current_thread().getName()) + '-' + str(real_num))
        in_q.task_done()

def consumer(in_q, out_q):  # 消费者
    headers = HEADERS
    while True:
        data = requests.get(url=in_q.get(), headers=headers)
        r = data.content
        content = str(r, encoding='utf-8', errors='ignore')
        soup = BeautifulSoup(content, 'html5lib')
        fixed_html = soup.prettify()
        html = etree.HTML(fixed_html)
        nums = html.xpath('//div[@class="col-md-1"]//text()')
        for num in nums:
            num = re.findall('[0-9]', ''.join(num))
            real_num = int(''.join(num))
            out_q.put(str(threading.current_thread().getName()) + '-' + str(real_num))
        in_q.task_done()  # 通知生产者，队列已消化完

def producer(in_q):  # 生产者
    ready_list = []
    while in_q.full() is False:
        for i in range(1, 1001):
            url = 'http://www.g.com/?page='+str(i)
            if url not in ready_list:
                ready_list.append(url)
                in_q.put(url)
            else:
                continue


if __name__ == '__main__':
    start = time.time()
    ########################## 多线程
    queue = Queue()
    result_queue = Queue()
    for i in range(1, 1001):
        queue.put('http://www.g.com?page='+str(i))
    print('queue 开始大小 %d' % queue.qsize())
    for index in range(10):
        thread = Thread(target=run, args=(queue, result_queue, ))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()
    queue.join()  # 队列消费完 线程结束
    ########################## 生产者消费者
    queue = Queue(maxsize=10)  # 设置队列最大空间为10
    result_queue = Queue()
    print('queue 开始大小 %d' % queue.qsize())
    producer_thread = Thread(target=producer, args=(queue,))
    producer_thread.daemon = True
    producer_thread.start()
    for index in range(10):
        consumer_thread = Thread(target=consumer, args=(queue, result_queue, ))
        consumer_thread.daemon = True
        consumer_thread.start()
    queue.join()  # 队列消费完 线程结束
    ########################## 多进程
    queue = multiprocessing.Manager().Queue()
    result_queue = multiprocessing.Manager().Queue()
    for i in range(1, 1001):
        queue.put('http://www.g.com2?page='+str(i))
    print('queue 开始大小 %d' % queue.qsize())
    pool = multiprocessing.Pool(10)  # 异步进程池（非阻塞）
    for index in range(1000):
        '''
        For循环中执行步骤：
        （1）循环遍历，将1000个子进程添加到进程池（相对父进程会阻塞）
        （2）每次执行10个子进程，等一个子进程执行完后，立马启动新的子进程。（相对父进程不阻塞）
         apply_async为异步进程池写法。异步指的是启动子进程的过程，与父进程本身的执行（爬虫操作）是异步的，
         而For循环中往进程池添加子进程的过程，与父进程本身的执行却是同步的。
        '''
        pool.apply_async(run, args=(queue, result_queue,))   # 维持执行的进程总数为10，当一个进程执行完后启动一个新进程.
    pool.close()
    pool.join()
    queue.join()  # 队列消费完 线程结束
    ##########################
    end = time.time()
    print('总耗时：%s' % (end - start))
    print('queue 结束大小 %d' % queue.qsize())
    print('result_queue 结束大小 %d' % result_queue.qsize())
