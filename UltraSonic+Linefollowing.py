import RPi.GPIO as GPIO
import time

slowest_speed = 10
low_speed = 12
mid_speed = 14
high_speed = 16

#assign GPIO pin to sensor
sensor1 = 21 #sensor from far left
sensor2 = 20 #sensor from left
sensor3 = 16 #sensor from middle
sensor4 = 26 #sensor from right
sensor5 = 25  #sensor from far right

#define and initialize variable to store senor output
sens1 = 0
sens2 = 0
sens3 = 0
sens4 = 0
sens5 = 0
#assign pins to sensor
TRIG = 22
ECHO = 27

#assign GPIO pin to motor
IN1 = 23 #set the direction of right wheel
IN2 = 24 #set the direction of right wheel
ENA = 12 #motor speed (pwm use for GPIO pin 12 and 13 for ena and enb)
IN3 = 17  #set the direction of left wheel
IN4 = 18  #set the direction of left wheel
ENB = 13  #motor speed

GPIO.setmode(GPIO.BCM) #set GPIO number in BCM mode
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
pwmFrequency = 20
right = GPIO.PWM(ENA, pwmFrequency) #set the pwm frequency (this for right wheels)
left = GPIO.PWM(ENB, pwmFrequency) #set the spwm frequency for left wheels)

def setup():
    #ultrasonic sensors
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    
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
    
def turnLeft(left_speed, right_speed):
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
       #ultrasonic Sensor
        GPIO.output(TRIG, False)
       # print ("Waiting For Sensor To Settle")
        time.sleep(0.5)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        avgDistance = 0
        distance = round(distance, 2)
        avgDistance=avgDistance+distance
        avgDistance=avgDistance/5
        
        print ("Distance: ",avgDistance,"cm")
        #if GPIO.input(sensor1) == 1(see white) then display 0 else GPIO.input(sensor1..5) == 0 (sense black) display 1
        sens1=0 if GPIO.input(sensor1) else 1
        sens2=0 if GPIO.input(sensor2) else 1
        sens3=0 if GPIO.input(sensor3) else 1
        sens4=0 if GPIO.input(sensor4) else 1
        sens5=0 if GPIO.input(sensor5) else 1
        sensorValue = ''.join([str(sens1), str(sens2), str(sens3), str(sens4), str(sens5)])
        print(sensorValue)
        time.sleep(0.1)
       # time.sleep(0.5)

#        moveForward(low_speed, low_speed)
       # turnRight(high_speed, mid_speed)
      #  turnLeft(mid_speed, high_speed)

       # moveForward(mid_speed, mid_speed)
#        time.sleep(1)
 #       stopCar()

#slight right turn
        if sensorValue == "00110" or sensorValue == "00111" or sensorValue == "01111" or sensorValue == "00101" or sensorValue == "01001":
            print("slight rught turn and forward")
            moveForward(high_speed, mid_speed)
#            time.sleep(0.5)
# forward
        if sensorValue == "00100" or sensorValue == "01110" or sensorValue == "01010" or sensorValue == "10001" or sensorValue == "11011":
            print(" move forward")
            moveForward(mid_speed,mid_speed)
#            time.sleep(0.5)
#slight left turn
        if sensorValue == "11100" or sensorValue == "01100" or sensorValue == "11110" or sensorValue == "10100" or sensorValue == "10010":
            print("slight left turn and forward")
            turnLeft(mid_speed, high_speed)
#            time.sleep(0.5)
#sharp left turn
        if sensorValue == "11000" or sensorValue == "10000" or sensorValue == "01000":
            print("sharp left turn")
            turnLeft(low_speed, high_speed)
#            time.sleep(0.5)
#sharp right turn
        if sensorValue == "00001" or sensorValue == "00010" or sensorValue == "00011":
            print("turning right")
            turnRight(high_speed, low_speed)
#            time.sleep(0.5)
#stop
        if  sensorValue == "00000" or avgDistance <2: 
            print("car stopping")
            stopCar()

#do something if every sensor reads 0
#        start = time.time()
#        if  sensorValue == "00000" and start >  time.time() + passed:
#            turnRight(high_speed, low_speed)

def destroy():
	GPIO.cleanup()
	
class lineFollowing():
	print('Program starting ..\n')
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
