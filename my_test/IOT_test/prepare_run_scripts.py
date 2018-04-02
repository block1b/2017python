# coding=utf8
# 运行模拟脚本
# 模拟数据，全传感器类型，值都为123,由准备的数据决定
# 全网关，全节点
from peewee_learn import data_prepare
from schemas_json_model import gateway_date
from marshmallow import Schema, fields, pprint
# 并行模拟器应使用多进程的方式进行模拟
# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程：
from multiprocessing import Pool
import os, time, random
from scripts_big_gateway import BigGatewatPut2_2


def long_time_task(url, apikey, data):
    print 'Run task %s (%s)...' % (apikey, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print "show url ", url  # 把要调用的外部方法在这里调用即可，可带参数
    BigGatewatPut2_2.http_put(url, apikey, data)
    print 'Task %s runs %0.2f seconds.' % (apikey, (end - start))

if __name__ == '__main__':

    # 生成大网关ids：[20180108001~20180108005]
    gateway_ids = data_prepare.get_big_gateway_ids("201801008", 1, 5)
    # print big_gateway_ids
    # 生成节点ids：[0108001~0108005]
    nodes = data_prepare.get_node_ids("0108", 1, 5)
    # print node_ids
    # 获取准备的传感器类型[all]
    attributes = data_prepare.attribute
    # print attribute
    # 获取所有带值传感器数据
    attribute_values = data_prepare.attribute_values
    # print attribute_values

    # 模拟脚本需要的数据段参数
    ggd = gateway_date.GetGatewayData(nodes=nodes, values=attribute_values)
    # pprint(ggd.result.data, indent=2)

    # 以上为参数
    print 'Parent process %s.' % os.getpid()
    p = Pool(100)  # pool默认并行4个进程，可设置Pool（n）,并发n个进程
    for a_gateway_id in gateway_ids:
        # 地址
        url_now = 'http://192.168.1.180:5858/gateway/up/' + a_gateway_id  # 目的地址
        # 数据
        gateway_data = ggd.result
        # api_key
        api_key = "123456"
        p.apply_async(long_time_task, args=(url_now, api_key, gateway_data,))

    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
