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
				if value.lower() == 'h': t = HIGH(usec, t, dry)
				if value.lower() == 'l': t = LOW(usec, t, dry)
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
        print command

	data = command['payload']
	cmd = command['command']

        # Setup PWM and DMA channel 0

	#PWM.set_loglevel(PWM.LOG_LEVEL_DEBUG)

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
