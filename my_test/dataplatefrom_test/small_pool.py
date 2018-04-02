# coding=utf8
# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程：
from multiprocessing import Pool
import os, time, random
from SmallGatewayClient1 import small_gateway_connect_server
from data_prepare import get_softgateway_ids
from my_heatbeat import get_my_id


def long_time_task(name):
    print 'Run task %s (%s)...' % (name, os.getpid())
    start = time.time()
    # time.sleep(random.random() * 3)
    small_gateway_connect_server(name)
    end = time.time()
    print 'Task %s runs %0.2f seconds.' % (name, (end - start))

if __name__ == '__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool(300)  # pool默认并行4个进程，可设置Pool（n）,并发n个进程

    # 网关api_key
    api_keys = get_softgateway_ids("1234123412340", 1, 300)

    for i in api_keys:
        heart = get_my_id(i)
        p.apply_async(long_time_task, args=(heart, ))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'

