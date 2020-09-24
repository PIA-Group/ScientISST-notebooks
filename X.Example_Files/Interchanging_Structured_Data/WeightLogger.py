from twisted.internet import protocol, reactor
from txws import WebSocketFactory
import json
import time

class WS(protocol.Protocol):
    def connectionMade(self):
        # Executed when the client successfully connects to the server.
        print("CONNECTED")
        self.loadLog()
        self.sendLog()
        print self.log
                
    def dataReceived(self, req):
        # Executed when the data is received from the client.
        print "< " + req
        data = json.loads(req)
        self.extendLog(float(data['weight']))
        self.sendLog()
        
    def connectionLost(self, reason):
        # Executed when the connection to the client is lost.
        print("DISCONNECTED")
        
    def loadLog(self):
        with open('WeightLogger.txt') as file:
            self.log = json.load(file)
            file.close()
            
    def sendLog(self):
        response = json.dumps(self.log)
        print "> " + response
        self.transport.write(response)
                        
    def extendLog(self, weight):
        date = time.strftime("%d-%m-%y %Hh:%Mm:%Ss")
        entry = [date, weight]
        self.log['weight'].append(entry)
        self.saveLog()
        self.sendLog()
        
    def saveLog(self):
        with open('WeightLogger.txt', 'w') as file:
            json.dump(self.log, file)
            file.close()


class WSFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return WS()


if __name__=='__main__':
    ip_addr, port = "127.0.0.1", 9000
    
    print("LISTENING AT %s:%s"%(ip_addr, port))

    connector = reactor.listenTCP(port, WebSocketFactory(WSFactory()))
    reactor.run()
