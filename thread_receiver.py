import numpy as np, pandas as pd, heartpy as hp
from communication_API import CommunicationAPI
from neural_network import NeuralNetwork, DriverStatus 

DIRECTORY_HEART_FEATURES = "user_heart_features"

class ThreadReceiver(CommunicationAPI):
    """ Class implemented by PC """
    def __init__(self):
        super().__init__(
            json_handler = self.receive_timeseries,
            threshold_reached_handler = None,
            port = 5556)
        self.knn = NeuralNetwork()
        self.features : dict = {}

    def receive_timeseries(self, json_data : dict):
        """ { handle the received json and compute the prediction } """
        input_features = self.knn.extract_features_from_json(json_data = json_data)
        prediction = self.knn.get_prediction(input_features)
        self.features = json_data
        self.features["prediction"] = str(prediction)
        self.write_features()
        print("Features: " + str(self.features))

    def write_features(self) :
        """ write in .csvFile the rr_intervals """
        with open(DIRECTORY_HEART_FEATURES + 'rr_intervals.csv', 'a') as file:
            file.write(str(self.features) + '\n')

    def fake_receive_timeseries(self, features):
        """ { handle the received json and compute the prediction } """
        prediction = self.knn.get_prediction(features)
        print("Prediction: " + str(prediction))

    def from_values_to_features(self, bpm, ibi, rmssd, sd, pnn50):
        return [[bpm, ibi, rmssd, sd, pnn50]]

    def process_ppg(self, data):
        sr = 100
        filtered = hp.filter_signal(data, [0.5, 15], sample_rate=sr, order=3, filtertype='bandpass')
        working_data, measures = hp.process_segmentwise(filtered, sample_rate=sr, segment_width=40, segment_overlap=0.25, segment_min_size=30)
        return  working_data, measures

    def load_drow_test(self):
        df = pd.read_csv('drow/ppg.csv')
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df = df.fillna(0)
        df.astype({'Red_Signal': 'int64'}).dtypes
        df.Red_Signal.rolling(50, min_periods=1).mean() # moving average
        data = df["Red_Signal"]

        working_data, measures = self.process_ppg(data)
        #['bpm', 'ibi', 'rmssd', 'sdnn', 'pnn50']
        print("DATI CON DROW 7 -> bpm = " + str(measures["bpm"]) + " , rmssd = " 
              + str(measures["rmssd"]) + " ,sd " + str(measures["sdnn"]) +
              " ,pnn50 = " + str(measures["pnn50"]) + ", ibi: " + str(measures["ibi"]))

        features = self.from_values_to_features(measures["bpm"][0], measures["ibi"][0], measures["rmssd"][0], measures["sdnn"][0], measures["pnn50"][0])

        self.fake_receive_timeseries(features=features)



# MAIN
thread_receiver = ThreadReceiver()
thread_receiver.load_drow_test()
thread_receiver.run()
