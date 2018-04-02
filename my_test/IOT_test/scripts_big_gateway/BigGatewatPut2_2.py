# -*- coding:utf-8 -*-
# File: http_put.py
# 类数据平台系统的大网管模拟器
import urllib2
import json
import sys


def http_put(url, api_key, data):
    try:
        json_data = json.dumps(data)
    except Exception as e:
        print e
        return None
    # 添加代理
    # proxy_support = urllib2.ProxyHandler({"http": "http://67.209.187.154:80"})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)

    request = urllib2.Request(url, json_data)
    
    request.add_header('api-key', api_key)
    request.add_header('Content-Type', 'application/json')
    
    request.get_method = lambda: 'POST'

    try:
        response = urllib2.urlopen(request, timeout=20000)
        print "success"
    except Exception as e:
        print 'bbb',e
        return None


if __name__ == '__main__':
    url_test = 'http://192.168.1.44:5858/gateway/up/0134567839600003'  # 目的地址
    
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

    gateway_api_key = 'xubaisenxubaisenxubaisenxubaisen'  # 网关号
    
    http_put(url=url_test, api_key=gateway_api_key, data=gateway_data)
