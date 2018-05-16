import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

while(True):
    print("Acendeu")
    GPIO.output(11,1)
    time.sleep(2)
    print("APagou")
    GPIO.output(11,0)
    time.sleep(2)
    
