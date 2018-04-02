# coding=utf8
# 通信协议
# 4字节 特殊字符0xF4F4F4F4
# 4字节 包体长度
# 4字节 包体数据类型
# 4字节 CMD
# 4字节 是否gzip
# 4字节 客户端平台定义
# 4字节 协议版本号
# 12字节 预留
# N字节  包体

import struct

HEAD_LEN = 40 # 包头的长度
MAGIC_NUM = 0xF4F4F4F4
BODY_DATA_TYPE_JSON = 1  # 包体为json
NOT_GZIP = 0  # 不用gzip压缩
CLIENT_PLATFORM_IOS = 1  # 客户端平台定义
PROTOCOL_VERSION = 1000  # 该协议的版本号


def pack_msg(cmd, msg):
    head = struct.pack('!10I',MAGIC_NUM,len(msg),BODY_DATA_TYPE_JSON,cmd,NOT_GZIP,\
                CLIENT_PLATFORM_IOS,PROTOCOL_VERSION,0,0,0)
    print len(head)
    return head+msg


def depack_msg(packed_msg):
    # 解析包头
    data = struct.unpack("!10I", packed_msg)
    return {
        'magic_num': data[0],
        'body_len': data[1],
        'body_data_type' : data[2],
        'cmd' : data[3],
        'is_gzip' : data[4],
        'client_platform' : data[5],
        'protocol_version' : data[6],
        'ext_int1' : data[7],
        'ext_int2' : data[8],
        'ext_int3' : data[9]
    }
