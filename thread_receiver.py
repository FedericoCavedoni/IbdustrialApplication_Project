import numpy as np, pandas as pd, heartpy as hp, json
from common.communication_API import CommunicationAPI
from common.driver_status import DriverStatus
from neural_network import NeuralNetwork
import random

DIRECTORY_HEART_FEATURES = "user_heart_features"
RASPBERRY_IP = "192.168.1.190"
RASPBERRY_PORT = "5555"

class ThreadReceiver(CommunicationAPI):
    """ Class implemented by PC """
    def __init__(self):
        super().__init__(
            json_handler = self.receive_timeseries,
            port = 5556)
        self.knn = NeuralNetwork()
        self.features : dict = {}
        self.prediction : DriverStatus = None

    def receive_timeseries(self, json_data : dict):
        """ { handle the received json and compute the prediction } """
        input_features = self.knn.extract_features_from_json(json_data = json_data)
        print("input_features ")
        self.print_features(input_features)
        self.prediction = self.knn.get_prediction(input_features)
        self.features = json_data
        self.features["prediction"] = str(self.prediction)
        print("Prediction: " + str(self.prediction))
        self.write_features()
        self.send_prediction_to_raspberry()
        
    def write_features(self) :
        """ write in .csvFile the rr_intervals """
        with open(DIRECTORY_HEART_FEATURES + 'rr_intervals.csv', 'a') as file:
            file.write(str(self.features) + '\n')

    def from_values_to_features(self, bpm, ibi, rmssd, sd, pnn50):
        """['bpm', 'ibi', 'rmssd', 'sdnn', 'pnn50']"""
        return [[bpm, ibi, rmssd, sd, pnn50]]

    def process_ppg(self, data) :
        """ process ppg signal """
        sr = 100
        filtered = hp.filter_signal(data, [0.5, 15], sample_rate=sr, order=3, filtertype='bandpass')
        working_data, measures = hp.process_segmentwise(filtered, sample_rate=sr, segment_width=40, segment_overlap=0.25, segment_min_size=30)
        return  working_data, measures

    def print_features(self, features):
        """ print features array ['bpm', 'ibi', 'rmssd', 'sdnn', 'pnn50']"""
        print("FEATURES -> bpm = " + str(features[0][0]) + " , ibi = " +
              str(features[0][1]) + " ,rmssd " + str(features[0][2]) +
              " ,sdnn = " + str(features[0][3]) + ", pnn50: " + str(features[0][4]))


    def send_prediction_to_raspberry(self):
        prediction_dict = {"prediction" : self.prediction}
        self.send_json(RASPBERRY_IP, RASPBERRY_PORT, json_data = json.dumps(prediction_dict))

# MAIN
thread_receiver = ThreadReceiver()
thread_receiver.run()
