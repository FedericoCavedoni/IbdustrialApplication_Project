import RPi.GPIO as GPIO
import time as Time
import threading
from sensor_driver import HRDriver
from communication_API import CommunicationAPI

GPIO_LED = 2
GPIO_HR = 3
THRESHOLD_SAMPLE = 250
hr_driver = HRDriver(GPIO_HR)

def receive_sample_result(json_data):
    """ Handler Classification Result """
    print("Classificazione battito ricevuta")

def send_new_record():
    """ Simula il raggiungimento della soglia per l'invio dei sample"""
    print("Comando threshold ricevuto")


def setup():
    """ setup function """
    print("setup function")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_LED, GPIO.OUT)
    hr_driver.setup()
    comm_api = CommunicationAPI(
        json_handler = receive_sample_result, 
        threshold_reached_handler = send_new_record)
    
    flask_thread = threading.Thread(target=comm_api.run)
    flask_thread.start()
    
    
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
