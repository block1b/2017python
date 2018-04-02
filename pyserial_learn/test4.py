# coding=utf8
# 发送一个，接收
import serial
# ser = serial.Serial("/dev/ttyACM0", 115200)
ser = serial.Serial("COM2", 115200)
flag = ser.isOpen()
print "打开串口：",flag


def hexShow(argv):
    result = ''
    hLen = len(argv)
    for i in xrange(hLen):
        hvol = ord(argv[i])
        hhex = '%02x' % hvol
        result += hhex+' '
    print 'hexShow:', result

while True:
    readstr = ser.read(2)
    # print ser.portstr
    hexShow(readstr)

