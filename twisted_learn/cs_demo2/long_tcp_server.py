# coding=utf8
# tcp长连接

"""
server程序
        1. 新连接和连接的断开
        2. 收包 解析
        3. 建立延迟检测是否登陆的任务
"""


import json

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.protocol import ServerFactory
import tool


def sign_in(msg, conn):
    """
        登陆
    :param msg:
    :param conn:
    :return:
    """
    uid = msg.get('uid')
    pwd = msg.get('pwd')
    if uid == 911 and pwd == 'dkjfkdjfkdjfkd':
        conn.setSignIn()  # signIn成功之后设置标记位
        print 'sign in success'
        pack_msg = tool.pack_msg(CMD_RESP['sign_in_resp'], json.dumps( {'is_sign_in':1} ) )
        conn.transport.write(pack_msg)
        return
    else:
        print 'user or pwd error'
        return -1


def heart_beat(msg, conn):
    '''
        心跳包
    :param msg:
    :return:
    '''
    print 'recv heart_beat from ', conn.transport.getPeer()
    return 0


CMD_MAP = {
    1000: sign_in,
    1001: heart_beat,
}

CMD_RESP = {
     'sign_in_resp': 8000   # sign in 的响应
}


class ClientProtocol(protocol.Protocol):

    def connectionMade(self):
        '''
            当客户端有新的连接的时候,会自动调用该方法
        :return:
        '''
        self.recv_data_buffer = ''   # 数据接受缓冲区
        self.is_sign_in = 0  # 初始上来的时候没有登陆
        print 'coming new connection =>', self.transport.getPeer()
        self.timeout_deferred = reactor.callLater(30, self.checkSignIn)   # 30秒之后调用checkSignIn方法

    def setSignIn(self):
        self.is_sign_in = 1

    def connectionLost(self, reason):
        '''
            当客户端连接断开的时候,会自动调用该方法
        :param reason:
        :return:
        '''
        print reason
        print 'connection is lost =>',self.transport.getPeer()

    def dataReceived(self, data):
        # 接收数据
        self.recv_data_buffer += data
        while True:
            # 如果缓冲区数据长度小于包头的长度
            if len(self.recv_data_buffer) < tool.HEAD_LEN:
                return
            # 继续解析包头
            head_data = tool.depack_msg(self.recv_data_buffer[:tool.HEAD_LEN])
            if head_data['magic_num'] != tool.MAGIC_NUM:
                # 没有按照规定的格式传输数据 不是正常的客户端  断开该连接
                self.transport.loseConnection()
            cmd = head_data['cmd']
            # 然后解析包体
            body_data = json.loads(self.recv_data_buffer[tool.HEAD_LEN:tool.HEAD_LEN+head_data['body_len']])
            # 数据已经接收完毕 清空缓冲区
            self.recv_data_buffer = ''
            # 根据cmd命令字处理具体逻辑
            if CMD_MAP.get(cmd):
                CMD_MAP[cmd](body_data, self)  # 这又是什么骚操作。哇骚气骚气，把变量名+（参数），作为函数调用
            # 每次执行完客户端请求后重置timeout，重新开始计算无操作时间。
            if self.timeout_deferred:
                self.timeout_deferred.cancel()
                self.timeout_deferred = reactor.callLater(30, self.checkSignIn)   # 30秒之后调用checkSignIn方法

    def checkSignIn(self):
        if not self.is_sign_in:
            self.transport.loseConnection()


class Factory(ServerFactory):

    pass


if __name__ == '__main__':
    factory = Factory()
    factory.protocol = ClientProtocol
    reactor.listenTCP(10231, factory)
    reactor.run()
