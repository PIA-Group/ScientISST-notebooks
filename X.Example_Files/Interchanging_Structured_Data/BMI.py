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
        result = self.calculateBMI(float(data['weight']), float(data['height']))
        response = json.dumps(result)
        print "> " + response
        self.transport.write(response)
        
    def connectionLost(self, reason):
        # Executed when the connection to the client is lost.
        print("DISCONNECTED")
        
    def calculateBMI(self, weight, height):
        result = dict()
        result['BMI'] = weight/((height/100)**2)
        if result['BMI'] < 18.5:
                result['category'] = 'Underweight'
        elif result['BMI'] >= 18.5 and result['BMI'] < 24.9:
                result['category'] = 'Normal'
        elif result['BMI'] >= 25 and result['BMI'] < 29.9:
                result['category'] = 'Overweight'
        else:
                result['category'] = 'Obesity'
        return result


class WSFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return WS()


if __name__=='__main__':
    ip_addr, port = "127.0.0.1", 9000
    
    print("LISTENING AT %s:%s"%(ip_addr, port))

    connector = reactor.listenTCP(port, WebSocketFactory(WSFactory()))
    reactor.run()
