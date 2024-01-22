import RPi.GPIO as GPIO
import time as Time

class HRDriver:
    """ class driver for the Heart Rate Sensor """
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin

    def setup(self):
        """ sensor driver setup """
        GPIO.setup(self.gpio_pin, GPIO.IN)
        GPIO.pinMode(self.gpio_pin, GPIO.INPUT_PULLDOWN)

    def read_sample(self):
        """ return sample value """
        return GPIO.digitalRead(self.gpio_pin)