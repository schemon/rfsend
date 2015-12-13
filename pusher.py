from ws4py.client.threadedclient import WebSocketClient
import all
import json
import time
import sys
import socket
import syslog
import logging
import logging.handlers
import urllib2

class DummyClient(WebSocketClient):
    @staticmethod
    def get_config():
    	return DummyClient.get_db()['config']
    @staticmethod
    def get_db():
	with open ("db", "a+") as db:
		print 'start load config'
    		try:
			data=json.loads(db.read())
			db.close()
			if data['id'] and data['config']:
				print 'file ok'
			else:
				print 'file corrupt'
				data = DummyClient.create_new_config()
		except:
			db.close()
			print 'failed'
			data = DummyClient.create_new_config()
		print data
		return data
	
    @staticmethod
    def create_new_config():
	with open ("db", "w+") as db:
		resp = urllib2.urlopen('http://52.28.7.161/device', '').read()
                data = json.loads(resp)
    		db.write(resp)
		return data
		db.close()
            
    def run(self):
	try:
		super(DummyClient, self).run()	
	except:
		msg = sys.exc_info()
                syslog.syslog(str(msg))
		print str(msg)

    def send(self, m, binary=False):
        if str(m) == 'beep': 
        	m = self.talk(str(m))
        else:
        	print "sent: " +str(m)
        	super(DummyClient, self).send(m)
    def talk(self, m):
	config = self.get_config()
        m = json.dumps({"event":"client-talk","data":{"name":"rpi","message":m},"channel": config['channel_name']})
        self.send(m)
    def opened(self):
        print 'connected'
    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        syslog.syslog(str(m))
        print m
	d = json.loads(str(m))

	event = d["event"]
	data = json.loads(d["data"])
	try:
		self.handleJsonMessage(data)
        	print 'handled'
	except ValueError: 
		print 'not json'		
	
        msg = "empty"
	

        if event == 'pusher:connection_established':
		config = self.get_config()
        	socket_id = data['socket_id']
                device_token = self.get_db()['id']
		resp = urllib2.urlopen('http://52.28.7.161/auth', 'deviceToken=' +device_token +'&socket_id=' +socket_id +'&channel_name=' +config['channel_name']).read()
                auth = json.loads(resp)['auth']
                m = json.dumps({"event":"pusher:subscribe","data":{"channel": config['channel_name'], "auth":auth}})
        	self.send(m)
	if msg == "ok":
		self.talk("Okidoki...")
	if msg == "hi": 
		1/0
		self.talk("oh herro!")
	if msg == "rpi": self.talk("yes?")
	if msg == "hello": self.talk("hi!")

    def handleJsonMessage(self, data):
	print data
	if 'message' in data:
        	command = json.loads(data['message'])
        	print 'found command: ', command
		all.send(command)
        	self.talk(json.dumps({"handled":command['name']}))
        else:
        	print 'did not find anything'
        	#self.talk("Unknwon command")

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
			config = DummyClient.get_config()
        		ws = DummyClient('ws://ws.pusherapp.com:80/app/' +config['pusher_key'] +'?protocol=7&client=rpi&version=0.0.1', None, None, 30)
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
		time.sleep(5)
	print " Script end"
	syslog.syslog('all_socket ended')

