# coding=utf-8
# 模拟接收端
import re
import binascii
from construct import Struct, OptionalGreedyRange, UBInt8, UBInt16, UBInt32, UBInt64
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, task

HOST = '192.168.1.106'
PORT = 5003

factory = None


class CommandParser:  # 命令解析器
    def __init__(self):
        self.constructFrame = Struct("parser",
                                     OptionalGreedyRange(
                                            Struct("packets",
                                                   UBInt8("header"),
                                                   UBInt16("plen"),
                                                   UBInt16("un_use1"),
                                                   UBInt64("nodeid"),
                                                   UBInt16("un_use2"),
                                                   UBInt16("un_use3"),
                                                   UBInt8("type"),
                                                   UBInt16("unit"),
                                                   UBInt8("value"),
                                                   UBInt32("undefined"),
                                                   UBInt8("sum")
                                                   )
                                     )
                                     )

    # 该函数是将控制报文中的可能需要转义的部分反转回来
    def convert(self, message):
        # not_escape_list = message[:28]
        # need_escape_list = re.findall(r'.{2}', message[28:][:-2]) # 去除可能转义的部分
        new_list = []
        bengin_list = message[:10]
        end_list = message[-26:]
        need_escape_list = re.findall(r'.{2}', message[10:-26])
        if len(need_escape_list) > 8:

            for index, item in enumerate(need_escape_list):
                if item == '7d':
                    pass
                elif need_escape_list[index-1] == '7d':
                    before_escape = self.unescape(item)
                    new_list.append(before_escape)
                else:
                    new_list.append(item)
        else:
            new_list = need_escape_list
        # print new_list

        raw_me_message = bengin_list + ''.join(new_list) + end_list
        # print raw_me_message
        return raw_me_message

    # 找回未转义的值
    def unescape(self, data):
        comparable_data = '0x20'
        decimal_num = int(data, 16)
        escaped_num = decimal_num ^ int(comparable_data, 16)
        return hex(escaped_num)[-2:]

    def construct_parse(self, bytestream):
        # 没有判断是否完整
        unescape_data = self.convert(bytestream)
        return self.constructFrame.parse(bytestream)

    def parse_pkgs(self, bytestream):
        container = self.construct_parse(bytestream)
        return container.packets
CommandParser = CommandParser()


class Echo(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        print "[x] I received the data:", binascii.b2a_hex(data)
        try:
            print self.factory.api_key
            new_data = CommandParser.parse_pkgs(data)[0]
            nodeid = new_data['nodeid']
            value = new_data['value']   
            print "[x] Controle NodeID:", nodeid
            print "[x] Value is :", value
        except Exception as e:
            new_data = ""
            print "[-] Command is ERROR!!!"


class EchoClientFactory(ClientFactory):

    def __init__(self):
        self.protocol = None

    def startedConnecting(self, connector):
        print('[+] Started to connect.')

    def buildProtocol(self, addr):
        print('[+] Connected.')
        self.protocol = Echo(self)
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print('[-] Lost connection.  Reason:', reason)
        self.protocol = None

    def clientConnectionFailed(self, connector, reason):
        print('[-] Connection failed. Reason:', reason)
        self.protocol = None


def send_data_demo(factory, my_id):  # my_id应当为一个参数
    # 首先判断是否存在一个 protococl 发送自己的ID
    if factory.protocol is not None:
        # my_id = '7E000925a1bcd5652e234d5c49'  # 上行一个节点身份验证
        my_id_hex = bytearray.fromhex(my_id)  # 转化格式
        factory.protocol.transport.write(str(my_id_hex))
        print "[+=] I send success..."
        return 
    else:
        print "[+=] I send fail.."
        return 


def small_gateway_connect_server(api_key):
    # 建立TCP连接
    factory = EchoClientFactory()
    factory.api_key = api_key
    reactor.connectTCP(HOST, PORT, factory)

    # 注册一个任务每隔几秒发送一个数据到server
    send = task.LoopingCall(send_data_demo, factory, api_key)
    send.start(5)

    reactor.run()

if __name__ == "__main__":
    my_id = '7e0009255f484a716577f53c6b'  # 上行一个节点身份验证
    small_gateway_connect_server(my_id)
