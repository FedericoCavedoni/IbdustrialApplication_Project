import RPi.GPIO as GPIO
import time as Time
from sensor_driver import HRDriver
from communication_API import CommunicationAPI

GPIO_LED = 2
GPIO_HR = 3
THRESHOLD_SAMPLE = 250
hr_driver = HRDriver(GPIO_HR)

def receive_sample_result(json_data : dict):
    """ Handler Classification Result """
    print("Classificazione battito ricevuta")

def threshold_reached_handler():
    """ Simula il raggiungimento della soglia per l'invio dei sample"""
    return


def setup():
    """ setup function """
    print("setup function")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_LED, GPIO.OUT)
    hr_driver.setup()
    comm_api = CommunicationAPI(receive_sample_result, threshold_reached_handler)
    
    
def loop():
    """ loop function """
    sample = 0
    old_sample = 0
    while True:
        sample = hr_driver.read_sample()
        if( (sample == GPIO.HIGH) and (old_sample != sample )):
            print("Battito")
            GPIO.output(GPIO_LED, GPIO.HIGH)
            Time.sleep(1)

        old_sample = sample
        GPIO.output(GPIO_LED, GPIO.LOW)


setup()
loop()
