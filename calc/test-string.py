#coding=utf-8

import re

def test1(content, src, des):
    """
    字符串 content 替换 src -> des 函数的设计和实现，如果需要在原串上替换呢？
    """
    if len(src) >= len(content) or src not in content:
        return src
    return content[0:content.index(src)] + des[0:len(src)] + content[content.index(src) + len(src)::]


def test2(ip0):
    """
    把字符串的IP地址变成32位整数的函数，要求能够检查各种输入错误。
    将：“127.0.0.1”转成 127*2^26 + 1;
    """
    try:
        str0 = ip0.split(".")
        return int(str0[3]) + int(str0[2]) * 256 + int(str0[1]) * 256 * 256 + int(str0[0]) * 256 * 256 * 256
    except:
        return ip0



if __name__ == "__main__":
    print test1("123ab789", "ab", "456")
    print test2("1.2.3.4")