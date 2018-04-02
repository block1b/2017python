# coding=utf8
# socket服务端
# 多线程
import socket
import threading
import time

# 只监听本机端口
ip = '127.0.0.1'
port = 9999


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 监听端口
s.bind((ip, port))

s.listen(5)  # 设置最大接入量


def tcplink(sock, addr):
    print "accept new connection from %s:%s" % addr
    sock.send('welcome')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send('hello, %s' % data)
    sock.close()
    print 'connection from %s:%s closed' % addr

while True:
    sock, addr = s.accept()

    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()


