import threading, json
import time as Time
import RPi.GPIO as GPIO
from sensor_driver import HRDriver
from communication_API import CommunicationAPI
from heart_beat_analysis import HeartBeatAnalysis
from neural_network import NeuralNetwork

GPIO_LED = 17
GPIO_HR = 4
PC_IP = "192.168.1.181"
PC_PORT = 5556

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
    global comm_api
    global hba
    #sample = 0
    #old_sample = 0
    while True:
        Time.sleep(1)
        # Ho campionato per 60s
        print("Numero campioni: " + str(len(hba.timeseries)))
        hba.compute_rr_intervals()
        if hba.session_duration_reached() :
            hba.copy__rr_intervals__in__temp_rr_intervals()
            with timeseries_lock:
                print("Svuotatao")
                hba.empty_arrays()
            # Features compuation
            hba.write_rrintervals()

            hba.compute_bpm()
            hba.compute_rmssd()
            hba.compute_standard_deviation()
            hba.compute_pnn()
            
            comm_api.send_json(PC_IP, PC_PORT, json_data = json.dumps(hba.features))


            #prediction_value = knn.get_prediction()
            #print("Predict_value = " + str(prediction_value))
            
            
            

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
    global comm_api
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
