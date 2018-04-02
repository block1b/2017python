# coding=utf8
# 透视，大概意思是，如果能控制连接的两端，可以直接用两端对象，不用硬套http协议
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
# Suppose you find yourself in control of both ends of the wire:
#  you have two programs that need to talk to each other,
#  and you get to use any protocol you want.
#  If you can think of your problem in terms of objects
# that need to make method calls on each other,
#  then chances are good that you can use
# Twisted's Perspective Broker protocol rather than
# trying to shoehorn your needs into something like HTTP,
# or implementing yet another RPC mechanism1.

from __future__ import print_function

from twisted.spread import pb
from twisted.internet import reactor


class Echoer(pb.Root):
    def remote_echo(self, st):
        print('echoing:', st)
        return st

if __name__ == '__main__':
    reactor.listenTCP(8789, pb.PBServerFactory(Echoer()))
    reactor.run()
