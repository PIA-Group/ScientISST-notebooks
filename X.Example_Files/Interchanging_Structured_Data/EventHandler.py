from twisted.internet import protocol, reactor
from txws import WebSocketFactory
import json

class WS(protocol.Protocol):
    def connectionMade(self):
        # Executed when the client successfully connects to the server.
        print("CONNECTED")
                
    def dataReceived(self, req):
        # Executed when the data is received from the client.
        print "< " + req
        data = json.loads(req)
        if data['event'] == "ACTION1":
            self.handleAction1(data['args'])
        elif data['event'] == "ACTION2":
            self.handleAction2(data['args'])
        elif data['event'] == "ACTION3":
            self.handleAction3(data['args'])
                                
    def connectionLost(self, reason):
        # Executed when the connection to the client is lost.
        print("DISCONNECTED")

    def handleAction1(self, args):
        self.transport.write("PYTHON EXECUTED ACTION 1")
        
    def handleAction2(self, args):
        self.transport.write("PYTHON EXECUTED ACTION 2")
        
    def handleAction3(self, args):
        self.transport.write("PYTHON EXECUTED ACTION 3")
        

class WSFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return WS()


if __name__=='__main__':
    ip_addr, port = "127.0.0.1", 9000
    
    print("LISTENING AT %s:%s"%(ip_addr, port))

    connector = reactor.listenTCP(port, WebSocketFactory(WSFactory()))
    reactor.run()
