# coding=utf8
# 用例：linux系统基于pyserial,串口调试脚本
# 目标：证明pyserial，在linux系统中可以进行正常通信
# 外部条件：外部设备arduino开发板，功能：将串口收到的数据发送回去
# 结果记录方式：写日志
# 约束：需要确认开发板可以收到一条完整的指令

import serial
# ser = serial.Serial("/dev/ttyACM0", 115200)
ser = serial.Serial("COM3", 115200)
flag = ser.isOpen()
print "打开串口：",flag
demo_str = '7E001610000102030405060708fffe00000100000300000000ca'
# str to bytes
byte_str = str.encode(demo_str)
demo = ser.write(byte_str)
print "发送", demo

# print "收到"
# print ser.read(19)

def hexShow(argv):
    result = ''
    hLen = len(argv)
    for i in xrange(hLen):
        hvol = ord(argv[i])
        hhex = '%02x' % hvol
        result += hhex+' '
    print 'hexShow:', result

readstr = ser.read(1)
# print ser.portstr
hexShow(readstr)