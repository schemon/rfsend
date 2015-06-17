from ws4py.client.threadedclient import WebSocketClient
import all
import json
import time
import sys
import socket
import syslog
import logging
import logging.handlers

class DummyClient(WebSocketClient):
    def run(self):
	try:
		super(DummyClient, self).run()	
	except:
		msg = sys.exc_info()
                syslog.syslog(str(msg))
		print str(msg)

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
	try:
		self.handleJsonMessage(json.loads(msg))
	except ValueError: 
		print 'not json'		
	
	print "got " +msg
	
	if msg == "ok":
		self.send("Okidoki...")
	if msg == "hi": 
		1/0
		self.send("oh herro!")
	if msg == "rpi": self.send("yes?")
	if msg == "hello": self.send("hi!")

    def handleJsonMessage(self, command):
	print command
	all.send(command)
        self.send("Command handled")

if __name__ == '__main__':
	# Setup syslog handler
	logger = logging.getLogger('ws4py')
	handler = logging.handlers.SysLogHandler()
	logger.addHandler(handler)

	syslog.syslog('starting')
	while True:    
		print 'connecting'
		syslog.syslog('connecting')
		try:
			name = "rpi"
        		ws = DummyClient('ws://infinite-refuge-5280.herokuapp.com/room/chat?username=' +name, None, None, 30)
        		ws.connect()
        		ws.run_forever()
    		except KeyboardInterrupt:
			syslog.syslog('KeyboardInterrupt sys.exit()')
        		ws.close()
			sys.exit()
		except socket.error:
			print 'socket error'
			syslog.syslog(LOG_WARNING, 'socket error')
		except:
			e = sys.exc_info()[0]
			syslog.syslog(LOG_CRIT, str(e))
		print 'lost connection'
		syslog.syslog('lost connection')
	print " Script end"
	syslog.syslog('all_socket ended')

