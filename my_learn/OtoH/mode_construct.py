# coding=utf-8

import re
import binascii
from construct import OptionalGreedyRange, UBInt8, UBInt64, UBInt16, Struct, Value, Container


# 小网关发送上来的数据解析 (心跳包) 得到小网关的APIkey信息
class SmallGatewayParser(object):
    def __init__(self):
        self.constructFrame = Struct('parser',
                                     OptionalGreedyRange(Struct('packets',
                                                                UBInt8('header'),
                                                                UBInt16('plen'),
                                                                UBInt8('functype'),
                                                                UBInt64('nodeid'),
                                                                UBInt8('sum'),
                                                                )
                                                         )
                                     )

    # 该函数是将控制报文中的可能需要转义的部分反转回来
    def convert(self, message):
        new_list = []
        begin_list = message[:8]
        end_list = message[-2:]
        need_escape_list = re.findall(r'.{2}', message[8:-2])
        if len(need_escape_list) > 8:
            for index, item in enumerate(need_escape_list):
                if item == '7d':
                    pass
                elif need_escape_list[index - 1] == '7d':
                    before_escape = self.unescape(item)
                    new_list.append(before_escape)
                else:
                    new_list.append(item)
        else:
            new_list = need_escape_list

        raw_me_message = begin_list + ''.join(new_list) + end_list
        return raw_me_message

    # 找回未转义的值
    @staticmethod
    def unescape(data):
        comparable_data = '0x20'
        decimal_num = int(data, 16)
        escaped_num = decimal_num ^ int(comparable_data, 16)
        return hex(escaped_num)[-2:]

    def construct_parser(self, bytestream):
        return self.constructFrame.parse(bytestream)

    def parse_pkgs(self, bytestream):
        container = self.construct_parser(bytestream)
        return container.packets

    # 得到节点号
    def get_node_id(self, bytestream):

        # 将二进制转为字符串
        str_data = binascii.b2a_hex(bytestream)

        # 获取转义之前的数据  去掉了校验位
        escape_data = self.convert(str_data)[:-2]

        # 小网关发送的数据的解析结果
        data = self.constructFrame.parse(bytestream)
        old_check_sum = data.get('packets')[0].get('sum')
        node_id = data.get('packets')[0].get('nodeid')

        if len(escape_data) is 24:
            # 转换为二进制
            ascii_data = bytearray.fromhex(escape_data)
            # 得到重新计算的校验位
            new_check_sum = CheckDigit.constructFrameParse.parse(ascii_data).get('checkSum')
            if old_check_sum == new_check_sum:
                return node_id

        else:
            return None


# 计算校验位
class CheckDigit(object):
    def __init__(self):
        self.constructFrameParse = Struct("parser",
                                          OptionalGreedyRange(UBInt8("packets")),
                                          Value("checkSum",
                                                lambda ctx: int((hex((255 - sum(ctx.packets[3:]))
                                                                     & 0xffffffffffffffff)[-3:-1]), 16))
                                          )


SmallGatewayParser = SmallGatewayParser()
CheckDigit = CheckDigit()

if __name__ == '__main__':
    """
    7e  
    000d  长度
    25    功能位
    007d 33 a2 00 40 71 53 bc   节点号
    50    校验位
    """
    # test_data = "7e000d250013a200407153bc65"
    test_data = "7E0009250013A200406EB0F0D7"
    test_data = "7e000d250a141e28323c465050"
    test_data = "7e000d250a141e28323c465014"
    test_data = "7e000d250013a200406eb0f0f6"
    ascii = bytearray.fromhex(test_data)

    # print SmallGatewayParser.get_node_id(ascii)
    s = SmallGatewayParser.get_node_id(ascii)
    # s = SmallGatewayParser.construct_parser(ascii)
    # print s

    H_sum = CheckDigit.constructFrameParse.parse(bytearray.fromhex("7e000d250a141e28323c4650")).checkSum
    print H_sum
    print hex(int(H_sum))
