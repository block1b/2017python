# coding=utf8

import json

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
import tool
from twisted.internet import task


online_protocol = []


def sign_in_resp(msg, conn):
    if msg.get('is_sign_in') == 1:
        print msg
        print 'very good, sign in success'
        # 创建定时的心跳任务
        t = task.LoopingCall(send_heart_beat,  *[conn])
        # 开启执行,每隔10秒执行一次
        t.start(10)


def send_heart_beat(conn):
    msg = {
    }
    conn.transport.write(tool.pack_msg(CMD['heart_beat'], json.dumps(msg)))

CMD = {
    'heart_beat': 1001,
}
CMD_RESP = {
    8000: sign_in_resp,   # sign in 的响应
}


class MyProtocol(Protocol):

    def connectionMade(self):
        '''
            客户端连接成功之后会自动调用该方法
        :return:
        '''
        print 'is already connect to the server'
        msg = {
            'uid': 911,
            'pwd': 'dkjfkdjfkdjfkd',
        }
        self.recv_data_buffer = ''
        cmd = 1000   # 定义1000表示登陆
        pack_msg = tool.pack_msg(cmd, json.dumps(msg))
        ret = self.transport.write(pack_msg)

    def dataReceived(self, data):
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
            print 'recv cmd',cmd
            # 然后解析包体
            body_data = json.loads(self.recv_data_buffer[tool.HEAD_LEN:tool.HEAD_LEN+head_data['body_len']])
            #  清空缓冲区
            self.recv_data_buffer = ''
            print 'recv body ', body_data
            # 根据cmd命令字处理具体逻辑
            if CMD_RESP.get(cmd):
                CMD_RESP[cmd](body_data, self)


class MyClientFactory(ClientFactory):

    protocol = MyProtocol

if __name__ == '__main__':

    reactor.connectTCP('127.0.0.1', 10231, MyClientFactory())
    reactor.run()
