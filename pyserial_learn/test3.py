import serial
ser = serial.Serial()


def hexShow(argv):
    result = ''
    hLen = len(argv)
    for i in xrange(hLen):
        hvol = ord(argv[i])
        hhex = '%02x' % hvol
        result += hhex+' '
    print 'hexShow:', result

ser.baudrate = 115200
ser.port = 'COM3'

ser.open()
readstr = ser.read(52)
# print ser.portstr
hexShow(readstr)