# coding=utf=8

# 对传感器数据的解析
# 入口数据 十六进制
from construct import Struct, OptionalGreedyRange, UBInt8, UBInt16, ULInt64
from construct import ULInt16, LFloat32
from construct.macros import Array


class MessageParse(object):
    def __init__(self):
        self.constructFrame = Struct("parser",
                                     OptionalGreedyRange(
                                         Struct("packets",
                                                UBInt8("header"),
                                                UBInt16("plen"),
                                                UBInt8("dir"),
                                                ULInt64("nodeid"),
                                                UBInt16("funcid"),
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
                                     OptionalGreedyRange(
                                         UBInt8("leftovers"),
                                     ),
                                     )

    def construct_parse(self, bytestream):
        return self.constructFrame.parse(bytestream)

    def parse_pkgs(self, bytestream):
        container = self.construct_parse(bytestream)
        return container.packets, container.leftovers

if __name__ == '__main__':
    # byte = "\x7e\x00\x1b\x55\x0c\x00\x60\x03\x01\x11\x00\x03\x50\x01\x01\x00\x01\x00\x00\x00\xa8" \
    #        "\x41\x02\x00\x02\x00\x85\xeb\xd1\x41\x59"

    # temp_data = "7e001b550c006003011100035001010001000000a8410200020085ebd14159"

    # byte = "\x7e\x00\x14\x55\x00\x00\x00\x2c\x00\x00\x00\x00\x50\x01\x01\x00\x01\x00\xed\x21\x01\x0d\xfd"

    # byte = "\x7e\x00\x14\x55\x00\x00\x00\x2c\x00\x00\x00\x00\x50\x01\x01\x00\x01\x00\xed\x21\x01\x0d\xfd"
    # byte = "\x7e\x00\x13\x55\x00\x00\x00\x18\x00\x00\x00\x00\x50\x01\x01\x00\x01\x00\xed\x21\x01\x0d\xff"

    # byte = "\x7e\x00\x13\x7e\x00\x13\x55\x01\x02\x03\x04\x05\x06\x07\x08\x50\x01\x01\x7e\x00\x13\x01\x00"
    byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 01 00 07 00 00 C0 7F 44 AA"
    byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 07 07 00 01 00 00 40 7D 20 4A "

    byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 07 00 01 00 00 40 7D 20 50 "

    byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 07 00 01 00 00 40 7D 20 50 37"

    byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 07 00 01 00 00 80 7F 44 EA"  # right 1022
    byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 07 00 01 00 00 C0 7F 44 AA"  # 1023
    byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 07 00 01 00 00 40 7F 44 2A"  # 1021

    byte = "7E 00 1B 55 01 02 03 04 05 06 07 08 50 01 07 00 01 00 00 40 7F 44 01 00 01 00 E6 97 BF 41 2A"   # 多数据

    # byte = "7E 00 13 55 01 02 03 04 05 06 07 08 50 01 07 00 01 00 00 C0 7C 44 AD"
    new_byte = bytearray.fromhex(byte)
    test = MessageParse()
    data, fler = test.parse_pkgs(new_byte)
    print data[0]
    print fler
