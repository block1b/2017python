# coding=utf8
# 本例用于测试,软网关数据展示部分
# byte数据转json格式

import json
import binascii
from MessageParse import MessageParse

"""解析后的报文数值参照表"""
data_type = {
    0: 'customize',
    1: 'tem',
    2: 'hum',
    3: 'gas',
    4: 'val',
    5: 'cur',
    6: 'fre',
    7: 'lig',
    8: 'pre',
    9: 'swi',
    10: 'wat',
    11: 'rai',
    12: 'res',
    13: 'tim',
    14: 'err',
    15: 'con'
}


class ByteToJson(object):
    # TODO 对于没有解析成功的只发送对应的原始数据,
    # TODO 而对于解析成功的 发送时要加上对应的最后一次的原始数据
    def __init__(self):
        self.leftovers = ""  # 定义不够解析的数据的保存位置

    def bytes_to_json(self, byte_data):
        """此函数实现从串口收上来的以7E开头的传感器数据转换成json数据"""
        data_parse, right_data = self.data_parse(byte_data)  # 解析数据
        data_pkgs = dict()  # 存放解析后的数据
        if data_parse:
            for data in data_parse[0].datas:
                if data:
                    sensor_type = data_type.get(data.type)  # 从参照表中得到数值含义
                    sensor_value = round(data.value, 6)
                    # TODO  还有很多数据类型......
                    if sensor_type == 'tem':
                        if (sensor_value > 100) or (sensor_value < -10):
                            sensor_value = 32.1  # block不应该写到这里加限制吧
                    if sensor_type is not None and sensor_value is not None:  # 注意判断条件，value会等与0
                        data_pkgs[sensor_type] = sensor_value

            if data_pkgs:  # 有数据才进行封装节点号(小端读取)  # block-e,默认的大端序读取
                str_data = binascii.b2a_hex(right_data)
                node_id = str_data[8:24]
                message = [node_id[i:i + 2] for i in range(0, len(node_id), 2)]
                message.reverse()  # 反序存储
                data_pkgs["sn"] = "".join(message)
                # 原始数据
                data_pkgs["origin_data"] = binascii.b2a_hex(byte_data)
            if data_pkgs:
                return self.build_json(data_pkgs)
        return

    def build_json(self, data):
        data_list = list()
        json_data = dict()
        try:
            data_list.append(data)
            json_data["datastreams"] = data_list
            json_data = json.dumps(json_data)
        except Exception as e:
            print e
        return json_data

    def data_parse(self, data):
        """此方法为接口，供外部调用。进行7e开头数据的解析，通过construct"""
        try:
            my_data = self.leftovers + data
            message_parse = MessageParse()
            pkgs, leftovers_list = message_parse.parse_pkgs(my_data)
            """
            如果当前数据(包括前一个不完整的报文+当前报文)解析成功，将保存不完整报文的leftovers数据置空；
            判断解析之后是否还有粘包的报文；
            如果有粘包就送到leftovers中，等待下一个报文到来。
            """
            if len(pkgs) != 0:
                if leftovers_list:
                    self.leftovers = bytearray.fromhex(
                        ''.join([binascii.b2a_hex(chr(item)) for item in leftovers_list])
                    )
                else:
                    self.leftovers = ''
                return pkgs, my_data

            self.leftovers += bytearray.fromhex(
                ''.join([binascii.b2a_hex(chr(item)) for item in leftovers_list])
            )
            # 在存储数据达到30字节的时候，找到最后一个7E进行裁剪，将7E之前的数据扔掉
            if len(self.leftovers) > 30:
                if self.leftovers.find(bytearray.fromhex("7e")) is -1:
                    self.leftovers = ''
            self.leftovers = self.leftovers[self.leftovers.rfind(bytearray.fromhex("7e")):]
        except Exception as ex:
            print ex
        return None, None


if __name__ == "__main__":
    b_t_j = ByteToJson()
    # str_data = "7e00135501020304050607085001000200020000000032"
    str_data = "7e00135501010000000000005001000101000000000032"
    # str_data = "7E0013550102030405060708500101000100D552CB4100"
    # str_data = "7e001355010203040506070850010b000b000000744269"
    byte_data = bytearray.fromhex(str_data)
    print b_t_j.bytes_to_json(byte_data)
