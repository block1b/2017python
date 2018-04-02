# coding=utf8
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
# 简单的服务端

from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def connectionMade(self):
        print 'coming new connection =>', self.transport.getPeer()

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        self.transport.write("server back:" + data)
        print "i received data:", data
        print "from :", self.transport.getPeer()


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000, factory)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
