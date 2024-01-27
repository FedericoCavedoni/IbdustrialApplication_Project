import threading
import time as Time
import RPi.GPIO as GPIO
from sensor_driver import HRDriver
from communication_API import CommunicationAPI
from heart_beat_analysis import HeartBeatAnalysis

GPIO_LED = 17
GPIO_HR = 4

timeseries_lock = threading.Lock()
hr_driver = HRDriver(GPIO_HR)
hba = HeartBeatAnalysis()
comm_api : CommunicationAPI = None

def setup():
    """ setup function """
    setup_gpio_pins()
    setup_communicationAPI()

def loop():
    """ loop function """
    #sample = 0
    #old_sample = 0
    while True:
        Time.sleep(1)
        
        print("Numero campioni: " + str(len(hba.timeseries)))
        hba.compute_rr_intervals()
        if(hba.session_duration_reached()):
            hba.write_rrintervals()
            
            with timeseries_lock:
                print("Distrutto")
                hba.deastroy_timeseries()
            # Qui va distrutto il vecchio contneuto: chiedi a chat come gestisco in modo corretto un array che viene modificato sia da un interrupt_handler che dal main?
        

        """
            sample = hr_driver.read_sample()
            if( (sample == GPIO.HIGH) and (old_sample != sample )): # if there is a new beat...
                heart_beat_timestamp = Time.time()
                hba.timeseries.append(heart_beat_timestamp)
                if(hba.t_differences_reached()): # Se ho raccolto un campionamento di 60 secondi
                    hba.compute_timeseries_intervals()
                    


                with open(TIMESTAMPS_FILE_NAME + '.csv', 'a') as file:
                    file.write(str(heart_beat_timestamp) + ',' + '\n')
                print("Battito")
                GPIO.output(GPIO_LED, GPIO.HIGH)
                Time.sleep(1)

            old_sample = sample
            GPIO.output(GPIO_LED, GPIO.LOW)
        """

def setup_gpio_pins():
    """ funzione di delegazione del setup. Il 'main' resta pulito """
    print("setup function")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_LED, GPIO.OUT)
    hr_driver.setup()
    hr_driver.set_interrupt_mode(timeseries = hba.timeseries,
                                 timeseries_lock = timeseries_lock,
                                 gpio_event = GPIO.RISING)

def setup_communicationAPI():
    """ setup delle API """
    comm_api = CommunicationAPI(
        json_handler = receive_sample_result,
        threshold_reached_handler = send_new_record)
    flask_thread = threading.Thread(target=comm_api.run)
    flask_thread.start()

def receive_sample_result(json_data):
    """ Handler Classification Result """
    print("Classificazione battito ricevuta")

def send_new_record():
    """ Simula il raggiungimento della soglia per l'invio dei sample"""
    print("Comando threshold ricevuto")




setup()
loop()
