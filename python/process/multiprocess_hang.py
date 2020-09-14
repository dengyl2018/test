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


stop = False

class Worker(multiprocessing.Process):
    u"""
    多进程方式执行任务，使用CPU密集型
    """
    def __init__(self):
        super(Worker, self).__init__()
        self.reset_ts = time.time() + 3
        self.stopping = False

    def run(self):
        logging.info('Process pid is %s' % os.getpid())

    def check_timeout(self, now):
        u"""
        若当前时间已超过复位时间，则结束进程
        :param now:
        :return:
        """
        global stop
        if now > self.reset_ts and not self.stopping:
            self.stopping = True
            logging.info('error pid is %s' % os.getpid())
            stop = True


def main():
    global stop
    worker_pool = []
    while 1:
        if worker_pool:
            now = time.time()
            for worker in worker_pool:
                worker.check_timeout(now)
                if stop:
                    logging.error('Process not run, exit!')
                    exit(-1)

        alive_workers = [worker for worker in worker_pool if worker.is_alive()]
        over_workers = list(set(alive_workers) ^ set(worker_pool))
        for over_worker in over_workers:
            over_worker.join()
        worker_pool = alive_workers
        if len(worker_pool) < 1000:
            logging.info('create worker')
            worker = Worker()
            worker.start()
            logging.info('worker pid is %s' % worker.pid)
            worker_pool.append(worker)
        time.sleep(0.001)


class ExecuteThread(threading.Thread):
    def run(self):
        main()

class ExecuteThread2(threading.Thread):
    def run(self):
        global stop
        while 1:
            logging.info('main thread')
            time.sleep(0.001)
            if stop:
                exit(-1)

if __name__ == '__main__':
    init_log('./timeout')
    main()

    # thread = ExecuteThread()
    # thread2 = ExecuteThread2()
    # thread.start()
    # thread2.start()
    # thread.join()
    # thread2.join()
