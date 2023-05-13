import RPi.GPIO as GPIO
import time 


# initalising the GPIOs the raspberry pi is connected to 
GPIO.setmode(GPIO.BCM)
TRIG = 17
ECHO = 27
LED = 18

# We need the Echo to read the distance (echolocation)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

maximum = 20
frequncy = 100

# setting up PWM for the led
pulse = GPIO.PWM(LED, frequncy)
pulse.start(0)


# read the calculation for the distance (this will be a function)

def duty_cycle(distance):
	inverse_dc = frequncy - ((distance / maximum) * 100) # using the mathematics from notes, create frequncy which can 
	pulse.ChangeDutyCycle(inverse_dc)

def distance():
	GPIO.output(TRIG, True)
	time.sleep(0.1) # this should be based on 1 microsecond
	GPIO.output(TRIG, False)
	
	start = time.time() # starting time is recorded and initalised
	
	while GPIO.input(ECHO) == 0: # sending echo
		start = time.time()
	
	while GPIO.input(ECHO) == 1: # echo is read and recieved
		end = time.time() 
	
	distance = ((end - start) * 34300) / 2 # converting into the form of cm
	duty_cycle(distance)
	
	return distance


	
# output the distance in the serial monitor
while distance() > 0:
	print(f"Distance: {round(distance(), 2)}")

