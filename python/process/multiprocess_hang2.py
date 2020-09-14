#coding=utf-8
import os
import time
import logging
import threading
import multiprocessing
import logging.handlers


def init_log(log_path, level=logging.INFO, when="midnight", backup=7,
             format="%(levelname)s:[%(asctime)s][%(filename)s:%(lineno)d][%(process)s][%(thread)d] %(message)s",
             datefmt="%Y-%m-%d %H:%M:%S"):
    formatter = logging.Formatter(format, datefmt)
    logger = logging.getLogger()
    logger.setLevel(level)

    dir = os.path.dirname(log_path)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class Worker(multiprocessing.Process):
    u"""
    多进程方式执行任务，使用CPU密集型
    """
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        logging.info('Process pid is %s' % os.getpid())
        x = y = 0
        for i in range(1, 100000):
            x += i
            y += i
        time.sleep(0.001)
        logging.info('Process pid is %s end' % os.getpid())
        


def main():
    for i in range(1, 100):
        logging.info('no. %s - create worker' % i)
        worker = Worker()
        worker.start()
        time.sleep(0.001)
        logging.info('no. %s - worker pid is %s, %s' % (i, worker.pid, worker.is_alive))
        


if __name__ == '__main__':
    init_log('./timeout')
    main()

    # thread = ExecuteThread()
    # thread2 = ExecuteThread2()
    # thread.start()
    # thread2.start()
    # thread.join()
    # thread2.join()
