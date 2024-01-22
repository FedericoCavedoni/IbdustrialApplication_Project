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



def loop():
    """ loop function """
    sample = 0
    old_sample = 0
    while True:
        sample = GPIO.digitalRead(GPIO_HR)
        if( (sample == GPIO.HIGH) and (old_sample != sample )):
            print("Battito")
            GPIO.output(GPIO_LED, GPIO.HIGH)
            Time.sleep(1)

        old_sample = sample
        GPIO.output(GPIO_LED, GPIO.LOW)


setup()
loop()
