from ws4py.client.threadedclient import WebSocketClient
import jula, clas
import json
import time
import sys
import socket

class DummyClient(WebSocketClient):
    def send(self, m, binary=False):
	m = json.dumps({"text": str(m)})
        print "sent: " +m
        super(DummyClient, self).send(m)
    def opened(self):
        #def data_provider():
        #    for i in range(1, 200, 25):
        #        yield "#" * i

        # for i in range(0, 200, 25):
        #    print i
            #self.send("*" * i)
        print 'connected'
    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        print m
	d = json.loads(str(m))
	msg = str(d["message"]).lower()
	
	if "on" in msg: 
                if "clas" in msg:
                        clas.send(0, 1)
			self.send("Lights should be bright!")
                elif msg == "on":
                        jula.send(0, 1)
			self.send("Lights should be bright!")	
		print "got " +msg
		
	if "off" in msg:
		if "clas" in msg:
			clas.send(0, 0)
		elif msg == "off":	 
			jula.send(0, 0)
		print "got " +msg
		self.send("Ok, lights dark  now...")
	if msg == "ok":
		self.send("Okidoki...")
	if msg == "hi": self.send("oh herro!")
	if msg == "rpi": self.send("yes?")
	if msg == "hello": self.send("hi!")
if __name__ == '__main__':
	while True:    
		print 'connecting'
		try:
			name = "rpi"
        		ws = DummyClient('ws://infinite-refuge-5280.herokuapp.com/room/chat?username=' +name, None, None, 30)
        		ws.connect()
        		ws.run_forever()
    		except KeyboardInterrupt:
        		ws.close()
			sys.exit()
		except socket.error:
			print 'socket error'
		print 'lost connection'
	print " Script end"

