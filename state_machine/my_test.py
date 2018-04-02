# coding=utf8
from escape import TransitionState

if __name__ == "__main__":
    s1 = "7E 00 02 25 7d 5e 12 7d 5e"  # 完整包
    l1 = []  # 结果集
    l2 = []  # 碎片集
    ts = TransitionState()
    # 任意字符串中抽取数据包（字符串）返回值：完整数据包
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
