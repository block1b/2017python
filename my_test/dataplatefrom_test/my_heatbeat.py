# coding=utf8
# 将api-key封装位心跳包
# 封包 例：7e 0009 25 0a141e28 323c4650 72 ## 7262 3859 7903 8285 60


import re
import binascii
from construct import OptionalGreedyRange, UBInt8, UBInt64, UBInt16, Struct, Value, Container


# 参数：重配置文件中得到的api—key（o）（string）
# 功能：将api-key封装位心跳包
def get_my_id(api_key):
    H_nodeid = re.sub('\s', '', api_key)  # 去除字符串中的空格
    # 将位数补足为偶数个！！！
    nodeid_len = len(H_nodeid)
    if nodeid_len % 2:
        nodeid_len += 1
    H_nodeid = H_nodeid.zfill(nodeid_len)
    # print H_nodeid
    # 计算包长
    H_nodeid_len = str(nodeid_len / 2 + 1).zfill(2)
    mode_string = "7e00" + H_nodeid_len + "25" + H_nodeid
    # mode_string = "7e00" + H_nodeid_len + "22" + H_nodeid
    # print mode_string

    # 计算校验位
    class Digit(object):
        def __init__(self):
            self.constructFrameParse = Struct("parser",
                                              OptionalGreedyRange(UBInt8("packets")),
                                              Value("checkSum",  # sum()可能有溢出错误，待定！！！
                                                    lambda ctx: str(hex((255 - sum(ctx.packets[3:]) & 0xff)))[2:].zfill(2)[-2:])
                                              )


    digit = Digit()
    H_sum = digit.constructFrameParse.parse(bytearray.fromhex(mode_string)).checkSum
    # print H_sum
    # print "sum= ", H_sum
    # 未转义的心跳包
    Heart = mode_string + H_sum
    # 转义
    new_heart = conver(Heart)
    return new_heart


# 转义 7e 7d 11 13 ,与20异或 标志位 7d
def conver(message):
    begin_list = message[:2]  #
    new_list = begin_list
    # 将字符串模拟成字节2个数一组
    need_escape_list = re.findall(r'.{2}', message[2:])

    for item in need_escape_list:
        if item in ['7d', '7e']:
            # 与‘20’异或
            item = str(hex(int(item, 16) ^ int("20", 16)))[2:]
            item = '7d' + item

        # 将转义后的字符串累加起来
        new_list = new_list + item
    # print "我的心跳包为：", new_list
    return new_list


if __name__ == "__main__":
    # 从配置文件获取api-key

    api_key = "1234 1234 1234 1234"
    #7e0005252b4985855c
    # api_key = "4c4f4954020400006000a718085a"
    # 将api-key封装为心跳包
    print get_my_id(api_key)
    #7e 0009 250a 141e 2832 3c46 50 72
