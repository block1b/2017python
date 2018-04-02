# coding=utf8

from construct import *
from construct import Struct, OptionalGreedyRange, UBInt8, UBInt16, ULInt64
from construct import ULInt16, LFloat32
from construct.macros import Array
import binascii

"""
    block-按照协议解析数据包
    参数：HEX_string;返回值：1个字典格式的解析结果，key就是结构中定义的名字,value(D)。
"""


class MessageParse(object):
    def __init__(self):
        self.constructFrame = Struct("parser",
                                     OptionalGreedyRange(
                                         Struct("packets",
                                                UBInt8("header"),
                                                UBInt16("plen"),
                                                UBInt8("functype"),
                                                ULInt64("nodeid"),
                                                UBInt16("apptype"),
                                                Array(lambda ctx: (ctx.plen - 1 - 8 - 2) / 8,
                                                      Struct("datas", ULInt16("type"),
                                                             ULInt16("unit"),
                                                             LFloat32("value"),
                                                             )
                                                      ),
                                                UBInt8("sum"),
                                                # UBInt8("simulation")
                                                ),
                                     ),
                                     # OptionalGreedyRange(
                                     #     UBInt8("right"),
                                     # ),
                                     )
        # 用于计算校验位，若与接收的校验位一致则验证通过。按字节接收累加求和。
        self.constructFrameCheckSum = Struct("parser",
                                             OptionalGreedyRange(UBInt8("packets")),
                                             Value("checkSum",
                                                   lambda ctx: (255 - sum(ctx.packets[3:-1]) & 0xff))

                                             )

    def construct_parse(self, hex_string):
        bytestream = bytearray.fromhex(hex_string)  # 将字符串转化为16进制字节流
        return self.constructFrame.parse(bytestream), self.constructFrameCheckSum.parse(bytestream).checkSum

    def parse_pkgs(self, bytestream):
        container, check_sum_result = self.construct_parse(bytestream)
        # 验证校验位    # 原结构支持多个数据包一起解析，V2版限制该功能，每次只处理一个数据包"packets[0]"
        if check_sum_result == container.packets[0].sum:
            return container.packets[0]
        else:
            return
        # return container.packets

if __name__ == "__main__":
    # byte = "7E 00 25 55 1000 0000 0000 0000 50 01 01 00 01 00 00 00 80 3f 02 00 02 00 00 00 80 3f 03 00 03 00 00 00 80 3f EC"
    # byte = "7E 00 25 55 01 02 03 04 05 06 07 08 50 01 01 00 01 00 00 00 80 3f 02 00 02 00 00 00 80 3f 03 00 03 00 00 00 80 3f EC"
    # byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 01 00 01 00 00 00 80 3F 74 7E 00 13 55 01 02 03 04 05 06 07 08 50 01 01 00 01 00 00 00 80 3F 74"
    byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 01 00 01 00 00 00 80 3F 74"
    # byte = "7E 00 13 55 01 00 00 00 00 00 00 00 50 01 01 00 01 00 00 00 80 3F 97"

    test = MessageParse()
    data = test.parse_pkgs(byte)
    # print data
    if data:
        # print data
        pass
    else:
        print "校验位错误，数据包无效！"

    # 获取value
    print data, type(data)
    print data.header, hex(data.header),  binascii.b2a_hex(bytearray.fromhex("0102030405060708"))
