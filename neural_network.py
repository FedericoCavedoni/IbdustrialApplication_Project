import joblib, subprocess, numpy as np
from common.driver_status import DriverStatus

class NeuralNetwork:
    """ Neural Network class"""
    def __init__(self):
        go_on = False
        while not go_on :
            try:
                self.model = joblib.load('model/model.joblib')
                go_on = True
                print("Model loaded correctly")
            except:
                print("Model file not found. Start the training...")
                subprocess.run(["python", "./project_network.py"])
                go_on = False
        self.array_features = {}
        self.prediction = 0
        

    # {features = ['bpm', 'ibi', 'rmssd', 'sdnn', 'pnn50']}
    def get_prediction(self, features) -> DriverStatus:
        """ return the presiction on the array_features """
        self.prediction = self.model.predict(features)
        return DriverStatus(self.prediction).name
    
    def extract_features_from_json(self, json_data : dict):
        """ extratcs the data from the dict in the order [bpm, ibi, rmssd, sdnn, pnn50] """
        
        bpm = json_data["bpm"]
        rr_intervals = list(map(float, json_data["rr_intervals"].split(',')))
        rmssd =  205.27957979875384 #json_data["rmssd"] * 7
        pnn50 = json_data["pNN"]
        sd = json_data["sd"]
        mean_rr_intervals = (np.average(rr_intervals)*1000) if len(rr_intervals) != 0 else 0
        return [np.array([bpm, mean_rr_intervals, rmssd, sd, pnn50])]