# coding=utf8
# 将10进制数字转化会16进制
# 封包 例：7e 0009 25 0a141e28 323c4650 72 ## 7262 3859 7903 8285
# 按照通信协议转义

import re
import binascii
from construct import OptionalGreedyRange, UBInt8, UBInt64, UBInt16, Struct, Value, Container


O_nodeid = "726238597903828560"
# 10进制转16进制
H_nodeid = str(hex(int(O_nodeid)))[2:-1]  # "0a14 1e28 323c 4650"
# 将位数补足16位
if len(H_nodeid) < 16:
    H_nodeid =H_nodeid.zfill(16)
print H_nodeid

mode_string = "7e000925" + H_nodeid
print mode_string


# 计算校验位
class Digit(object):
    def __init__(self):
        self.constructFrameParse = Struct("parser",
                                          OptionalGreedyRange(UBInt8("packets")),
                                          Value("checkSum",
                                                lambda ctx: str(hex((255 - sum(ctx.packets[3:])))).zfill(2)[-2:])
                                          )


digit = Digit()
H_sum = digit.constructFrameParse.parse(bytearray.fromhex(mode_string)).checkSum
print H_sum

# 心跳包未转义
Heart = mode_string + H_sum
print Heart


# 7e000925 0a14 1e28 323c 4650 72 13->7d33
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

test_data = "7e0009250a141e28323c46507213"
print conver(test_data)