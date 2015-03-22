from RPIO import PWM
import getopt, time

pin = 4
T = 250

def sendData(data):
        t = 0
	t += START(t)
        for x in data:
                if x is "0": 
			t += ZERO(t)
			t += ONE(t)
                if x is "1": 
			t += ONE(t)
			t += ZERO(t)
        t += STOP(t)

	return t


def START(t):
	return write(11, t)

def STOP(t):
	return write(41, t)

def ZERO(t):
	return write(2, t)
	
def ONE(t):
	return write(6, t)

def write(wait, t):
	PWM.add_channel_pulse(0, pin, t, T)
        return T*wait

def send(unit, command):
        # Setup PWM and DMA channel 0
        PWM.setup(1, 0)
        cycle_length = 110000
        PWM.init_channel(0, cycle_length)

        data = "0100 1000 0110 1001 1111 1111 100" +command +" " +unit
        for i in xrange(3):
                sendData(data)
                time.sleep(0.1)
	print data


        PWM.clear_channel_gpio(0, pin)

        # Shutdown all PWM and DMA activity
        PWM.cleanup()


	return True
	

