# coding=utf8
# 将api-key封装位心跳包
# 封包 例：7e 0009 25 0a141e28 323c4650 72 ## 7262 3859 7903 8285 60


import re
import binascii
from construct import OptionalGreedyRange, UBInt8, UBInt64, UBInt16, Struct, Value, Container


# 16进制字符串切片，emmm好像麻烦了，直接切片就好了
class Digit(object):
    def __init__(self):
        self.constructFrameParse = Struct("parser",
                                          OptionalGreedyRange(UBInt8("packets")),
                                          )


if __name__ == "__main__":

    # self.leftovers += bytearray.fromhex(
    #     ''.join([binascii.b2a_hex(chr(item)) for item in leftovers_list])
    # )
    leftovers_list = [5, 10, 13]
    # 将整数转16进制字符串
    print ([binascii.b2a_hex(chr(item)) for item in leftovers_list])
    # 将整数转16进制字符串  # [2:].zfill(2)[-2:] 只取最后一个字节
    HEX_str = hex(578437695752307201)
    print HEX_str
    print int(HEX_str[:-1], 16)

    hex_string = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 01 00 01 00 00 00 80 3F 74"
    bytestream = bytearray.fromhex(hex_string)  # 将字符串转化为16进制字节流

    digit = Digit()
    packets = digit.constructFrameParse.parse(bytestream).packets

    # print packets
    print ([hex(i)[2:].zfill(2)[-2:] for i in packets])

    # 切片2 2切片emmm不要自己造轮子
    print [hex_string]
    hex_string = re.sub('\s', '', hex_string)  # 去除字符串中的空格
    # hex_string必须是偶数个字符
    print re.findall(r'.{2}', hex_string)  # 每2个切片

    HEX = "0001"
    print int(HEX, 16)

    a = bytearray.fromhex("1122")
    b = bytearray.fromhex("3344")
    c = a+b
    d = binascii.b2a_hex(c)
    e = binascii.b2a_hex(d)

    print d, type(d), e, type(e)

    print len(c)
    print c[1:2]

    print binascii.b2a_hex("1")
