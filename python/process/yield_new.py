#coding=utf-8

import time

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            print("n is none.")
            continue
        print("consumer: %s" % n)
        time.sleep(1)
        r = 'consumer %s finished.' % n

def producer(consumer):
    consumer.next()
    for i in xrange(0, 5):
        r = consumer.send(i)
        print("producer %s" % r)
    consumer.close()
    

producer(consumer())
