# coding=utf8
# emmm学习twisted的先修课
# 客户端 访问新浪
import socket


ip = 'www.sina.com.cn'
port = 80

# 创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接
s.connect((ip, port))

# 发送请求
s.send('GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

# 接收数据
buffer = []
while True:
    d = s.recv(1024)  # 每次最多接收1个字节
    if d:
        buffer.append(d)
    else:
        break

data = ''.join(buffer)

# 关闭连接:
s.close()

header, html = data.split('\r\n\r\n', 1)
print header

# 把接收的body写入文件:emm文件太大，浏览器解析不出来
with open('sina.html', 'wb') as f:
    f.write(html)

