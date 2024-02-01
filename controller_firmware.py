import threading, json
import time as Time
import RPi.GPIO as GPIO
from sensor_driver import HRDriver
from common.communication_API import CommunicationAPI
from common.driver_status import DriverStatus
from heart_beat_analysis import HeartBeatAnalysis
from heart_beat_analysis import MAX_INTERVAL_BETWEEN_BEATS

GPIO_LED = 17
GPIO_HR = 4
PC_IP = "192.168.1.181"
PC_PORT = 5556

blinking_condition = threading.Condition()
new_beat_reeived = threading.Condition()
hr_driver = HRDriver(GPIO_HR)
hba = HeartBeatAnalysis()
comm_api : CommunicationAPI = None
there_is_abnormal : int = 0
shared_timestamp = [0]

def setup():
    """ setup function """
    setup_gpio_pins()
    setup_communicationAPI()

def loop():
    """ loop function """
    global comm_api
    global hba
    while True:
        wait_for_new_beat()
        hba.timeseries.append(shared_timestamp[0])
        print("Numero campioni: " + str(len(hba.timeseries)))
        if(len(hba.timeseries) >= 2):
            beat_interval = hba.timeseries[-1] - hba.timeseries[-2]
            if((beat_interval * 1000) >= MAX_INTERVAL_BETWEEN_BEATS):
                print("INVALID SESSION")
                hba.empty_arrays()
                wake_thread_blink()
                continue
        hba.compute_rr_intervals()
        if hba.session_duration_reached() :
            #hba.copy__rr_intervals__in__temp_rr_intervals()
            # Features compuation
            #hba.write_rrintervals()

            hba.compute_bpm()
            hba.compute_rmssd()
            hba.compute_standard_deviation()
            hba.compute_pnn()
            
            comm_api.send_json(PC_IP, PC_PORT, json_data = json.dumps(hba.features))

            hba.empty_arrays()

            #prediction_value = knn.get_prediction()
            #print("Predict_value = " + str(prediction_value))
            
            
def setup_gpio_pins():
    """ funzione di delegazione del setup. Il 'main' resta pulito """
    print("setup function")
    global shared_timestamp
    shared_timestamp[0] = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_LED, GPIO.OUT)
    led_off()
    hr_driver.setup()
    hr_driver.set_interrupt_mode(shared_timestamp = shared_timestamp,
                                 wake_condition = new_beat_reeived,
                                 gpio_event = GPIO.RISING)

def setup_communicationAPI():
    """ setup delle API """
    global comm_api
    comm_api = CommunicationAPI(json_handler = receive_sample_result)
    flask_thread = threading.Thread(target=comm_api.run)
    flask_thread.start()

def receive_sample_result(json_data):
    """ Handler Classification Result """
    print("Classificazione battito ricevuta ->" + str(json_data))
    prediction : DriverStatus = json_data["prediction"]
    if prediction == DriverStatus.ABNORMAL.name :
        wake_thread_blink()
    write_log(prediction)

def write_log(prediction : DriverStatus):
    hba.write_features(prediction = prediction)


def wait_for_new_beat():
    with new_beat_reeived:
        new_beat_reeived.wait()

def blinking():
    " This is the body-thread for blinking the led in case of abnormality of the car-driver "
    while(True):
        with blinking_condition:
            blinking_condition.wait()
        blink_number = 5
        while(blink_number > 0):
            led_on()
            Time.sleep(0.3)
            led_off()
            Time.sleep(0.3)
            blink_number -= 1

blink_thread = threading.Thread(target = blinking)
blink_thread.start()

def wake_thread_blink():
    with blinking_condition:
        blinking_condition.notify()

def led_on():
    "Turn on the led"
    GPIO.output(GPIO_LED, GPIO.HIGH)

def led_off():
    "Turn off the led"
    GPIO.output(GPIO_LED, GPIO.LOW)


setup()

loop()
