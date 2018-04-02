# coding=utf8
# 并行模拟器应使用多进程的方式进行模拟
# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程：
from multiprocessing import Pool
import os, time, random
import BigGatewatPut2_2


def long_time_task(url, apikey, data):
    print 'Run task %s (%s)...' % (apikey, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print "show apikey ", apikey  # 把要调用的外部方法在这里调用即可，可带参数
    BigGatewatPut2_2.http_put(url, apikey, data)
    print 'Task %s runs %0.2f seconds.' % (apikey, (end - start))

if __name__ == '__main__':
    url_test = 'http://192.168.1.180:5858/gateway/up/0134567839600003'  # 目的地址
    # 测试数据
    # 模拟网关2 两个节点，分别接入温度传感器
    gateway_data = {
        "node_datas": [{
            "node_id": "0300110203600018",
            "node_attributes": {
                "hum": "10.770000", "tem": "19.200002"
            }
        },
            {
                "node_id": "0300110103700025",
                "node_attributes": {
                    "hum": "10.780000", "tem": "19.200003"
                }
            }]
    }

    print 'Parent process %s.' % os.getpid()
    p = Pool()  # pool默认并行4个进程，可设置Pool（n）,并发n个进程
    # fish = [1, 2, 3, 4, 5]  # 开启多进程的个数
    # 从文件获取进程标识
    bf = BaseFile()
    fish = bf.read_file("biggateway_api_keys.csv")

    for a_dict in fish:
        a_api_key = a_dict["gateway_api_key"]  # 如下args可以传递参数
        p.apply_async(long_time_task, args=(url_test, a_api_key, gateway_data,))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
