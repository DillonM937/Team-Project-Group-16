import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
servo1 = GPIO.PWM(12, 50)
servo1.start(2)
dump = False;

x = input("Do you want to dump container?");
if x == "y":
    servo1.ChangeDutyCycle(7);
    time.sleep(4)
    servo1.ChangeDutyCycle(2);
    servo1.stop()
    GPIO.cleanup()
else: x = input("Do you want to dump container?");
