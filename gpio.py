
import RPi.GPIO as GPIO
import signal
import sys
import time
import zmq
import json

TRIG = 23
ECHO = 24
context = None;
socket = None;

def setupDevices():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	print "Calibrating sensors"
	GPIO.output(TRIG, False)
	print "Waiting For Sensor To Settle"
	time.sleep(2)
	

def setupZMQ():
	global context,socket
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.bind("tcp://127.0.0.1:5000")

setupDevices()
setupZMQ()


def run_program():
	global context,socket

	while True:
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		v =0
		while GPIO.input(ECHO)==0:
			pulse_start = time.time()

		while GPIO.input(ECHO)==1:
			if v ==0 :
				v = 1;
				continue
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)

		# data = {}
		# data['distance1'] = distance;
		# data = json.dumps(data);
		data = "distance1"+ " " +str(distance)
		print data
		socket.send(data)

		time.sleep(0.5)





def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    try:
    	if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
    		sys.exit(1)
    except KeyboardInterrupt:
    	print("Ok ok, quitting");
    	GPIO.cleanup()
    	sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    run_program()


