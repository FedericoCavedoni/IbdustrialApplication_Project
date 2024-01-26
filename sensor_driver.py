import RPi.GPIO as GPIO
import time as Time

class HRDriver:
    """ class driver for the Heart Rate Sensor """
    def __init__(self, gpio_pin):
        self._gpio_pin = gpio_pin
        self.timeseries : [] = None

    def setup(self):
        """ sensor driver setup """
        GPIO.setup(self._gpio_pin, GPIO.IN)  # Definiamo quel gpio_pin come pin di Input
        GPIO.pinMode(self._gpio_pin, GPIO.INPUT_PULLDOWN) # Attiviamo la resistenza interna di PullDown

    def read_sample(self):
        """ return sample value """
        return GPIO.digitalRead(self._gpio_pin)
    
    def set_interrupt_mode(self, timeseries : [], gpio_event = GPIO.RISING, interrupt_handler = None):
        """ la funzione abilita la modalità di gestione ad Interrupt per il sampling """
        self.timeseries = timeseries
        GPIO.add_event_detect(self._gpio_pin,
                              gpio_event,
                              callback = self._default_ISR if (interrupt_handler is None) else interrupt_handler,
                              bouncetime=300) # 300 è l'interrivalTime (sovra-stimato) fra 2 battiti consecutivi, ipotizzando un bpm massimo di 220.
    
    def _default_ISR(self):
        """ default Interrupt Service Routine per il sampling """
        timestamp = Time.time()
        print("_default_ISR()" + timestamp)
        if(self.timeseries):
            self.timeseries.append(timestamp)
        else:
            print("_default_ISR FALSE")