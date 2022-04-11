import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BCM)#set GPIO number in BCM mode

forward_speed = 10
low_speed = 12
mid_speed = 14
high_speed =16

#assign GPIO pin to sensor
sensor1 = 21 #sensor from far left
sensor2 = 20 #sensor from left
sensor3 = 16 #sensor from middle
sensor4 = 26 #sensor from right
sensor5 = 25  #sensor from far right

#sensors for Ultrasonic
TRIG = 22
ECHO = 27


#define and initialize variable to store senor output
sens1 = 0
sens2 = 0
sens3 = 0
sens4 = 0
sens5 = 0

#assign GPIO pin to motor
IN1 = 23 #set the direction of right wheel
IN2 = 24 #set the direction of right wheel
ENA = 12 #motor speed (pwm use for GPIO pin 12 and 13 for ena and enb)
IN3 = 17  #set the direction of left wheel
IN4 = 18  #set the direction of left wheel
ENB = 13  #motor speed

#ultrasonic sensor
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setmode(GPIO.BCM) #set GPIO number in BCM mode
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
pwmFrequency = 20
right = GPIO.PWM(ENA, pwmFrequency) #set the pwm frequency (this for right wheels)
left = GPIO.PWM(ENB, pwmFrequency) #set the spwm frequency for left wheels)

def setup():
    GPIO.setup(sensor1, GPIO.IN) #setup sensor as input
    GPIO.setup(sensor2, GPIO.IN)
    GPIO.setup(sensor3, GPIO.IN)
    GPIO.setup(sensor4, GPIO.IN)
    GPIO.setup(sensor5, GPIO.IN)

    GPIO.setup(IN1, GPIO.OUT) #setup motor control pin as output
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    
def changeSpeed(left_speed, right_speed):
    right.ChangeDutyCycle(right_speed) #change right wheel speed
    left.ChangeDutyCycle(left_speed) #change left wheel speed
    
#to stop car
def stopCar():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    changeSpeed(0,0)
#move forward    
def moveForward(left_speed, right_speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    changeSpeed(left_speed, right_speed)

def turnLeft (left_speed, right_speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    changeSpeed(left_speed, right_speed)

def turnRight(left_speed, right_speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    changeSpeed(left_speed, right_speed)
    
def loop():

    right.start(15) #control the speed
    left.start(15)

    while True:

        #if GPIO.input(sensor1) == 1(see white) then display 0 else GPIO.input(sensor1..5) == 0 (sense black) display 1
        sens1=0 if GPIO.input(sensor1) else 1
        sens2=0 if GPIO.input(sensor2) else 1
        sens3=0 if GPIO.input(sensor3) else 1
        sens4=0 if GPIO.input(sensor4) else 1
        sens5=0 if GPIO.input(sensor5) else 1
        sensorValue = ''.join([str(sens1), str(sens2), str(sens3), str(sens4), str(sens5)])
        print(sensorValue)
        time.sleep(0.5)

        avgDistance= 0
        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        print ("Waiting for Ultrasonic Sensor to Settle")
        time.sleep(2)                                   #Delay

        GPIO.output(TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                           #Delay of 0.00001 seconds
        GPIO.output(TRIG, False)

                				#Set TRIG as LOW
        while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
        distance = round(distance,2)                 #Round to two decimal points
        if distance < 15:      #Check whether the distance is within 15 cm range
            stopCar()
            time.sleep(1)

	 #slight right turn
        elif sensorValue == "00110" or sensorValue == "00111" or sensorValue == "01111":
            print("I'm going slightly right")
            moveForward(mid_speed, low_speed)
	#sharp left turn
        elif sensorValue == "10000" or sensorValue == "01000" or sensorValue == "11000":
            print("sharp left turn")
            turnLeft(low_speed, mid_speed)
	#turning right
        elif sensorValue == "00001" or sensorValue == "00010" or sensorValue == "00011":
            print ("turning right")
            turnRight(mid_speed, low_speed)
        else:
            moveForward(forward_speed, forward_speed)


def destroy():
	GPIO.cleanup()
	
class lineFollowing():
	print('Program starting ..\n')
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

