from websocket import create_connection
ws = create_connection("ws://infinite-refuge-5280.herokuapp.com/room/chat?username=pi")
print "Sending 'Hello, World'..."
ws.send("Hello, World")
print "Sent"
print "Reeiving..."
result =  ws.recv()
print "Received '%s'" % result
ws.close()

