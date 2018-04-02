# coding=utf8
# 将api-key封装位心跳包
# 封包 例：7e 0009 25 0a141e28 323c4650 72 ## 7262 3859 7903 8285 60


import re
import binascii
from construct import OptionalGreedyRange, UBInt8, UBInt64, UBInt16, Struct, Value, Container


# 参数：重配置文件中得到的api—key（o）（string）
# 功能：将api-key封装位心跳包
def get_my_id(api_key):
    # O_nodeid = "726238597903828560"
    O_nodeid = api_key
    # 10进制转16进制
    H_nodeid = str(hex(int(O_nodeid)))[2:-1]  # "0a14 1e28 323c 4650" hex后的数位若超过整型，会转为long会多L，就简单的方法就是够长。
    # 将位数补足为偶数个！！！
    nodeid_len = len(H_nodeid)
    if nodeid_len % 2:
        nodeid_len += 1
    H_nodeid = H_nodeid.zfill(nodeid_len)
    # print H_nodeid
    # 计算包长
    H_nodeid_len = str(nodeid_len / 2 + 1).zfill(2)
    mode_string = "7e00" + H_nodeid_len + "25" + H_nodeid

    # print mode_string

    # 计算校验位
    class Digit(object):
        def __init__(self):
            self.constructFrameParse = Struct("parser",
                                              OptionalGreedyRange(UBInt8("packets")),
                                              Value("checkSum",
                                                    lambda ctx: str(hex((255 - sum(ctx.packets[3:])) & 0xff))[2:].zfill(2)[-2:])
                                              )


    digit = Digit()
    H_sum = digit.constructFrameParse.parse(bytearray.fromhex(mode_string)).checkSum
    # print H_sum

    # 未转义的心跳包
    Heart = mode_string + H_sum
    # 转义
    new_heart = conver(Heart)
    return new_heart


# 转义 7e 7d 11 13 ,与20异或 标志位 7d
def conver(message):
    begin_list = message[:8]  # 前8位是固定写法不会需要转义
    new_list = begin_list
    # 将字符串模拟成字节2个数一组
    need_escape_list = re.findall(r'.{2}', message[8:])

    for item in need_escape_list:
        if item in ['7d', '7e', '11', '13']:
            # 与‘20’异或
            item = str(hex(int(item, 16) ^ int("20", 16)))[2:]
            item = '7d' + item

        # 将转义后的字符串累加起来
        new_list = new_list + item

    return new_list


if __name__ == "__main__":
    # 从配置文件获取api-key
    # import os
    # import ConfigParser
    #
    # cf = ConfigParser.ConfigParser()
    # if os.path.exists("./setting.ini"):
    #     cf.read("./setting.ini")  # 未完待定
    #     if cf.get("ip", "apikey"):
    #         owner = cf.get("ip", "apikey")
    # else:
    #     raise ("error")
    api_key = ["6238597903828561",
               "6238597903828562",
               "6238597903828563"]
    for temp in api_key:

    # 将api-key封装为心跳包
        print get_my_id(temp)
