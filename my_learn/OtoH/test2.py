# coding=utf8
# 计算校验位


def calc_checksum(s):
    sum = 0
    for c in s:
        sum += ord(c)
    sun = -(sum % 256)
    return '%2X' % (sum & 0xff)

print calc_checksum('1')