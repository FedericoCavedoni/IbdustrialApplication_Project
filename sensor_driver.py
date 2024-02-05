import time as Time
import threading
import RPi.GPIO as GPIO

BLINKING_PERIOD = 0.3

class HRDriver:
    """ class driver for the Heart Rate Sensor """
    def __init__(self, gpio_pin_hr, gpio_pin_led):
        self._gpio_pin = gpio_pin_hr
        self._gpio_pin_led = gpio_pin_led
        self.timeseries : [] = None
        self.shared_timestamp = None
        self.wake_condition : threading.Condition = None
        self.blink_thread : threading.Thread = None
        self.blinking_condition : threading.Condition = None

    def setup(self):
        """ sensor driver setup """
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self._gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  # Attivo la resistenza interna di PullDown
        
        GPIO.setwarnings(False)
        GPIO.setup(self._gpio_pin_led, GPIO.OUT)
        self.blinking_condition = threading.Condition()
        self.blink_thread = threading.Thread(target = self._blinking)
        self.blink_thread.start()

    def read_sample(self):
        """ ritorna il valore digitale letto dal gpio_pin. DA USARE SOLO IN MODALITA' POLLING """
        return GPIO.digitalRead(self._gpio_pin)
    
    def set_interrupt_mode(self, shared_timestamp, wake_condition, gpio_event = GPIO.RISING, interrupt_handler = None):
        """ la funzione abilita la modalità di gestione ad Interrupt per il sampling """
        self.shared_timestamp = shared_timestamp
        self.wake_condition = wake_condition

        GPIO.add_event_detect(self._gpio_pin,
                              gpio_event,
                              callback = self._default_ISR if (interrupt_handler is None) else interrupt_handler,
                              bouncetime = 260) # The real MinimumInterrivalTime is 270mS -> equivalent to 220BPM.

    def _default_ISR(self, channel):
        """ default Interrupt Service Routine per il sampling. It's body must be short as much as possible. """
        self.shared_timestamp[0] = Time.time()
        with self.wake_condition:
            self.wake_condition.notify()
        comp_time = Time.time() - self.shared_timestamp[0] # ONLY FOR COMPUTATION TIME ANALYSIS
        with open('ComputationTime_ISR.csv', 'a') as file:             # ONLY FOR COMPUTATION TIME ANALYSIS
            file.write(str(comp_time) + "\n")  # ONLY FOR COMPUTATION TIME ANALYSIS

    def led_on(self):
        "Turn on the led"
        GPIO.output(self._gpio_pin_led, GPIO.HIGH)

    def led_off(self):
        "Turn off the led"
        GPIO.output(self._gpio_pin_led, GPIO.LOW)

    def blink(self):
        """ This functions wakes the blinking_thread """
        with self.blinking_condition:
            self.blinking_condition.notify()

    def _blinking(self):
        " This is the body-thread for blinking the led in case of abnormality of the car-driver "
        while True :
            with self.blinking_condition:
                self.blinking_condition.wait()
            _blink_number = 5
            while _blink_number > 0 :
                self.led_on()
                Time.sleep(BLINKING_PERIOD)
                self.led_off()
                Time.sleep(BLINKING_PERIOD)
                _blink_number -= 1
