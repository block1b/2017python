# coding=utf8
# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程：
from multiprocessing import Pool
import os, time, random
from BigGatewatPut1 import http_put
from data_prepare import get_softgateway_ids


def long_time_task(name, url, api_key, gateway_data):
    print 'Run task %s (%s)...' % (name, os.getpid())
    start = time.time()
    # time.sleep(random.random() * 3)
    http_put(url=url, api_key=api_key, data=gateway_data)
    end = time.time()
    print 'Task %s runs %0.2f seconds.' % (name, (end - start))

if __name__ == '__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool()  # pool默认并行4个进程，可设置Pool（n）,并发n个进程

    # 测试数据
    url = 'http://192.168.1.106:5004'
    # 网关数据
    value = 1.1
    gateway_data = {"datastreams": [{"sn": "030011020001000b", "tem": value},
                                    {"sn": "030011020001000b", "hum": value},
                                    {"sn": "030011020001000b", "val": value},

                                    ]
                    }

    # 网关的IP
    api_keys = get_softgateway_ids("1234123412340", 1, 300)

    for i in api_keys:
        p.apply_async(long_time_task, args=(i, url, i, gateway_data))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'

