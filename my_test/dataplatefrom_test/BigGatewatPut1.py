# -*- coding:utf-8 -*-
# File: http_put.py

import urllib2
import json
import sys


def http_put(url, api_key, data):
    # 删除代理设置
    # proxy_handler = urllib2.ProxyHandler({})
    # opener = urllib2.build_opener(proxy_handler)
    # urllib2.install_opener(opener)

    try:
        json_data = json.dumps(data)  # 此处把没用的0除去了例0.27000变为0.27,并将数据类型转化为字符串。以标准的格式编码（encode）
    except Exception as e:
        print e
        return None
    
    request = urllib2.Request(url, json_data)  # 指定额外的数据发送到服务器，数据应该是缓存在一个标准的application/x-www-form-urlencoded格式
    
    request.add_header('apiKey', api_key)  # 附加header
    request.add_header('Content-Type', 'application/json')
    
    request.get_method = lambda: 'PUT'  # HTTP的请求方法

    try:
        res = urllib2.urlopen(request, timeout=2)  # 打开请求对象，超时
        print "success", res.read()
    except Exception as e:
        print "bbb",e
        return None


if __name__ == '__main__':
    # url = 'http://127.0.0.1:5001'  # ？_？
    url = 'http://192.168.1.106:5004'
    # 网关1 两个节点，分别接入温度传感器 030011020001000b节点号sn tem:温度
    gateway_data = { "datastreams": [ { "sn": "030011020001000b", "tem": 0.750000 },
                              { "sn": "030011020001000b", "hum": 0.750000 },
                              { "sn": "030011020001000b", "val": 0.750000 },

                              ]
             }

    # gateway_api_key = 'a5hwdyjcrbg57jst46vwxgmzee3wzq8g'  # 网关的IP
    gateway_api_key = '2222'
    # from ScriptsGatewaySystem.bingxinggateway import test8
    # gateway_data = test8.get_data(2)
    http_put(url=url, api_key=gateway_api_key, data=gateway_data)

    # learn_this_file
    # json_data = json.dumps(gateway_data)
    # print type(json_data)

