from RPIO import PWM
import getopt, time

pin = 4
T = 250
CHANNEL = 0

def sendData(data, command, dry = False):
	t = 0
        for x in data:
		if x in command:
			for c in command[x]:
				value = str(c['v'])
				usec = c['u']
				print value, usec
				if value == 'h': t = HIGH(usec, t, dry)
				if value == 'l': t = LOW(usec, t, dry)
		elif command != ' ':
			print 'Missing ', x
	return t


def LOW(length, t, dry):
	#if not dry: print 'LOW  ', length, ' ', t
	return t + length

def HIGH(length, t, dry):
	if not dry:
		#print 'HIGH ', length, ' ', t
		PWM.add_channel_pulse(CHANNEL, pin, t, length)
        return t + length

def send(command):
	#unit = "{:04b}".format(unit)

	#data = "0100 1000 0110 1001 1111 1111 100" +str(command) +" " +unit
        #data = "0010 0000 0001 0010 0110 1011 100" +str(command) +" " +unit
        #data = "S 0101 1011 0110 0100 0100 0000"
        #data = "S 0101 1001 0000 1000 1001 0000"
        print command
        if command is 0:
                data = "S 0101 1011 0110 0100 0100 0010"
        else:
                data = "S 0101 1110 1001 0101 0001 0010"

	#data = "A 0010 0000 0001 0010 0110 1011 100" +str(command) +" " +unit +"B"
	#cmd = {'1': [('H', 250), ('L', 1250), ('H', 250), ('L', 250)], '0': [('H', 250), ('L', 250), ('H', 250), ('L', 1250)], 'A': [('H', 250), ('L', 2500)], 'B':[('H', 250), ('L', 10000)]}
	cmd = {'1': [('H', 1000), ('L', 500)], '0': [('H', 500), ('L', 1000)], 'S': [('H', 2600), ('L', 7250)]}

	import json
	cmd = json.loads('{"1": [{"v":"H", "u":1000}, {"v":"L","u":500}], "0": [{"v":"H", "u":500}, {"v":"L","u":1000}], "S": [{"v":"H", "u":2600}, {"v":"L","u":7250}]}')
        data = data + data +data

	data = command['payload']
	cmd = command['command']

        # Setup PWM and DMA channel 0

	PWM.set_loglevel(PWM.LOG_LEVEL_DEBUG)

        if PWM.is_setup():
		print "setuped"
                #PWM.cleanup()
	else:
		print "not setuped"
		PWM.setup(1, CHANNEL)

	if PWM.is_channel_initialized(CHANNEL):
		print "was init"
        	#PWM.clear_channel_gpio(CHANNEL, pin)
		#PWM.clear_channel(CHANNEL)
	else:
		print "not init" 
		cycle_length = sendData(data, cmd, True)
		cycle_length = 250000
		print 'cycle length ', cycle_length
        	PWM.init_channel(CHANNEL, cycle_length)

	start = time.time()
        sendData(data, cmd)
	time.sleep(0.25)
	print "Process time: " + str(time.time() - start)
	print data

        PWM.clear_channel_gpio(CHANNEL, pin)

	return True
	
def cleanup():
	PWM.cleanup()
	return True
