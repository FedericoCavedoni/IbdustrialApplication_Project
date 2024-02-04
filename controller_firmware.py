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
new_beat_reeived = threading.Condition()
hr_driver = HRDriver(GPIO_HR, GPIO_LED)
hba = HeartBeatAnalysis()
comm_api : CommunicationAPI = None
shared_timestamp = [0]

time1 = 0
time2 = 0

def setup():
    """ setup function """
    setup_gpio_pins()
    setup_communicationAPI()

def loop():
    """ loop function """
    global comm_api
    global hba
    global time1
    global time2
    while True:
        # Il nostro Sporadic task ha un MinimumInterrivalTime, ossia ~272mS.
        if (time2 - time1) > 0.270: # 0.270S
            print("Deadline mancata")
        if not wait_for_new_beat() :    # if not... means that there is no hands on the steering wheel
            print("Please, take hands on the Steering Wheel!")
            hba.empty_arrays()
            hr_driver.blink()
            continue
        time1 = Time.time()
        hba.timeseries.append(shared_timestamp[0]) # --> As soon as this threas is waked-up, we read the shared variable
        print(".")
        hba.compute_rr_intervals()
        if hba.session_duration_reached() :
            # Features compuation
            hba.compute_bpm()
            hba.compute_rmssd()
            hba.compute_standard_deviation()
            hba.compute_pnn()
            
            comm_api.send_json(PC_IP, PC_PORT, json_data = json.dumps(hba.features))

            hba.empty_arrays()
            print("\n")
        time2 = Time.time()


def setup_gpio_pins():
    """ funzione di delegazione del setup. Il 'main' resta pulito """
    print("Setup GPIO pins")
    global shared_timestamp
    shared_timestamp[0] = 0
    hr_driver.setup()
    hr_driver.led_off()
    hr_driver.set_interrupt_mode(shared_timestamp = shared_timestamp,
                                 wake_condition = new_beat_reeived,
                                 gpio_event = GPIO.RISING)

def setup_communicationAPI():
    """ setup delle API """
    print("Setup API")
    global comm_api
    comm_api = CommunicationAPI(json_handler = receive_sample_result)
    flask_thread = threading.Thread(target=comm_api.run)
    flask_thread.start()

def receive_sample_result(json_data):
    """ Handler Classification Result """
    print("Driver Condition: " + str(json_data["prediction"]))
    prediction : DriverStatus = json_data["prediction"]
    if prediction == DriverStatus.ABNORMAL.name :
        hr_driver.blink()
    write_log(prediction)

def write_log(prediction : DriverStatus):
    """ write log on permanent memory (SD) """
    hba.write_features(prediction = prediction)

def wait_for_new_beat():
    """ this function blocks on that Condition the thread that invokes it """
    with new_beat_reeived:
        return new_beat_reeived.wait(MAX_INTERVAL_BETWEEN_BEATS)


setup()
loop()
