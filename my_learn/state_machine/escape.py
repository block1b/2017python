# coding=utf-8

import escape_sm
import re
import copy


class TransitionState(object):

    _fsm = None
    length = 0
    string = ""
    garbage_collect = None
    result = None
    status = False

    def __init__(self):
        self._fsm = escape_sm.Transition_sm(self)
        self.length = 0
        self.string = ""
        self.garbage_collect = list()
        self.result = list()

    def set_status(self):
        self.status = True

    def data_init(self):
        self.length = 0
        self.string = ""
        self.status = False

    def append(self, string):
        if self.status:
            self.string += self.xor(string)
            self.status = False
        else:
            self.string += string

    @staticmethod
    def xor(data, default="0x20", base=16):
        decimal_num = int(data, base)
        escape_num = hex(decimal_num ^ int(default, base))[-2:]
        return escape_num.upper()

    def getLength(self):
        return len(self.string)/2

    def getMSG_len(self):
        return self.length

    def gc(self):
        if self.string:
            self.garbage_collect.append(self.string)
        self.data_init()

    def collect(self):
        if self.string:
            self.result.append(self.string)

    def calcLen(self):
        self.length = int(self.string[-4:], 16)

    def EOS(self):
        if self.string:
            self.garbage_collect.append(self.string)
        self.data_init()
        self._fsm.setState(self._fsm._States[0])  # 初始化状态机的状态为等待状态
        result = copy.deepcopy(self.result)
        garbage_collect = copy.deepcopy(self.garbage_collect)
        self.result = list()
        self.garbage_collect = list()
        return result, garbage_collect

    def Checkstring(self, string):

        self._fsm.enterStartState()
        string = string.upper().replace(" ", "")
        need_escape_list = re.findall(r'.{2}', string)
        for byte in need_escape_list:
            self._fsm.next_char(byte)

        if need_escape_list and need_escape_list[-1] == "7D":
            if self.string:
                self.string += "7D"
        return self.EOS()


sm = TransitionState()


if __name__ == '__main__':
    s1 = "7E 00 02 25 7d 5e 12 7d 5e"  # 完整包
    l1 = []  # 结果集
    l2 = []  # 碎片集
    ts = TransitionState()
    (l1, l2) = ts.Checkstring(s1)
    print l1, l2
    s2 = "7E 00 03 25 7d 5e 7d 5d 7d"  # 缺省校验位
    (l1, l2) = ts.Checkstring(s2)
    print l1, l2

    s3 = "7E 00 03 25 7d 5e 12 7d 5e 7E 00 03 25 7d 5e 7d 5d 7d 7E 00 03 25 7d 5e 7d 5d 7d"  # 后包不完整
    (l1, l2) = ts.Checkstring(s3)
    print l1, l2

    s4 = "7E 00 03 25 7d 5e 7d 5d 7d 7E 00 03 25 7d 5e 12 7d 5e "  # 前包不完整
    (l1, l2) = ts.Checkstring(s4)
    print l1, l2

    s5 = "7E 00 03 25 7d 5e 12 7d 5e 7E 00 03 25 7d 5e 12 7d 5e"  # 多个包
    (l1, l2) = ts.Checkstring(s5)
    print l1, l2

