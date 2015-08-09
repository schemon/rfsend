from ws4py.client.threadedclient import WebSocketClient
import all
import json
import time
import sys
import socket
import syslog
import logging
import logging.handlers
from hashlib import *
import hmac

class DummyClient(WebSocketClient):
    def run(self):
	try:
		super(DummyClient, self).run()	
	except:
		msg = sys.exc_info()
                syslog.syslog(str(msg))
		print str(msg)

    def send(self, m, binary=False):
        print "sent: " +str(m)
        super(DummyClient, self).send(m)
    def talk(self, m):
        m = json.dumps({"event":"client-talk","data":m,"channel":"presence-rpi"})
        self.send(m)
    def opened(self):
	#im = json.dumps({"event":"pusher:subscribe","data":{"channel":"presence-rpi"}})
        #self.send(m)
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

	event = d["event"]
	data = json.loads(d["data"])
	try:
		#self.handleJsonMessage(json.loads(data))
        	print 'handled'
	except ValueError: 
		print 'not json'		
	
        msg = "empty"
	

        if event == 'pusher:connection_established':
		print type(data)
        	socket_id = data['socket_id']
        	print 'socket_id ' +socket_id
		string_to_sign = socket_id +':private-rpi'
		secret = '76a57ea82e311bcbbb1f'
		digest = hmac.new(secret, string_to_sign, sha256).hexdigest()
                print 'digest ', digest
        	key = '599cb5ed77cd5efb659a'
        	auth = key +':' +digest
                m = json.dumps({"event":"pusher:subscribe","data":{"channel":"private-rpi", "auth":auth}})
        	self.send(m)
	if msg == "ok":
		self.talk("Okidoki...")
	if msg == "hi": 
		1/0
		self.talk("oh herro!")
	if msg == "rpi": self.talk("yes?")
	if msg == "hello": self.talk("hi!")

    def handleJsonMessage(self, command):
	print command
	if 'payload' in command:
		all.send(command)
        	self.talk("Command handled")
        else:
        	self.talk("Unknwon command")

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
        		ws = DummyClient('ws://ws.pusherapp.com:80/app/599cb5ed77cd5efb659a?protocol=7&client=rpi&version=0.0.1', None, None, 30)
        		ws.connect()
        		ws.run_forever()
    		except KeyboardInterrupt:
			syslog.syslog('KeyboardInterrupt sys.exit()')
        		ws.close()
			sys.exit()
		except socket.error:
			print 'socket error'
			syslog.syslog('socket error')
		except:
			e = sys.exc_info()[0]
			syslog.syslog(str(e))
		print 'lost connection'
		syslog.syslog('lost connection')
	print " Script end"
	syslog.syslog('all_socket ended')

