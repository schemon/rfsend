from ws4py.client.threadedclient import WebSocketClient
import jula
import json
import time

class DummyClient(WebSocketClient):
    def opened(self):
        def data_provider():
            for i in range(1, 200, 25):
                yield "#" * i

        #self.send(data_provider())

        for i in range(0, 200, 25):
            print i
            #self.send("*" * i)

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        print m
	d = json.loads(str(m))
	msg = d["message"]
	if msg == "on": 
		jula.send(14, 1)
		print "got on"
	if msg == "off": 
		jula.send(14, 0)
		print "got off"

if __name__ == '__main__':
    try:
	name = "pi-" +str(time.time())
        ws = DummyClient('ws://infinite-refuge-5280.herokuapp.com/room/chat?username=' +name)
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()

