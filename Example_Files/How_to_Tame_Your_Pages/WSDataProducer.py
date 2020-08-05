from twisted.internet import protocol, reactor
from txws import WebSocketFactory
from pylab import *
import thread
import time


class WS(protocol.Protocol):
    def connectionMade(self):
        print("CONNECTED")
        # Launch code running independently in a thread (runs while self.run is True)
        self.run = True
        thread.start_new_thread(dataProducer, (self,))

    def dataReceived(self, req):
        pass
        
    def connectionLost(self, reason):
        print("DISCONNECTED")
        # Signal independent code to stop
        self.run = False
        
    def sendMessage(self, msg):
        self.transport.write(msg)
        print(msg)

                
class WSFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return WS()

        
# Receives as input parameter a reference to the connection
def dataProducer(conn):
    n = 500
    while conn.run:
        time.sleep(n/1000.)
        data = array([arange(n), rand(n)])
        conn.sendMessage(str(data.T.tolist()))
        

if __name__=='__main__':
    ip_addr, port = "127.0.0.1", 9000
    
    print("LISTENING AT %s:%s"%(ip_addr, port))

    connector = reactor.listenTCP(port, WebSocketFactory(WSFactory()))
    reactor.run()
