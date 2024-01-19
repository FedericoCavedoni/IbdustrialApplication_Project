import RPi.GPIO as GPIO
import time as Time

GPIO_LED = 2
GPIO_HR = 3

def setup():
    """ setup function """
    print("setup function")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_LED, GPIO.OUT)
    GPIO.setup(GPIO_HR, GPIO.IN)


setup()

while True:
    GPIO.output(2, GPIO.HIGH)
    Time.sleep(1)
    GPIO.output(2, GPIO.LOW)
    Time.sleep(1)
    