# coding=utf8
# 对construct的初步学习

import re
import binascii
from construct import OptionalGreedyRange, UBInt8, UBInt64, UBInt16, Struct, Value, Container


# 计算校验位
class Digit(object):
    def __init__(self):
        self.constructFrameParse = Struct("parser",
                                          OptionalGreedyRange(UBInt8("packets")),
                                          )


digit = Digit()
mode_string = "7e0009250a141e28323c4650"  # sum=72
O_digit_bit = digit.constructFrameParse.parse(bytearray.fromhex(mode_string))  # 拆分为字节长度的10进制数字
O_packets = O_digit_bit.get("packets")
print O_packets
O_sum = 255 - sum(O_packets[3:])
# 好吧，不知道为什么要再跟0xff & 操作,负数与正数&的结果不同
H_sum = str(hex(O_sum & 0xff)).zfill(2)[-2:]
print H_sum
# 坑 当计算可变长段的和与FF接近范围在F内的时候，就会造成一位校验位，切片规则只要后两位的写法会照成错误。所以先补全为两位
# 坑 当使用10进制的数与16进制的数进行&操作的时候，负数正数的到的结果不同，需要了解正负数在计算机中的储存原理！！！
# 将16进制负数转为正数的方法是与0xff & 操作。

d1 = 5
d2 = hex(d1 & 0xff)
print d2[2:].zfill(2)
