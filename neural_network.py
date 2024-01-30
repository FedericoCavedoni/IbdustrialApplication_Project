import joblib
from sklearn.neighbors import KNeighborsClassifier

class NeuralNetwork:
    """ Neural Network class"""
    def __init__(self):
        self.model = joblib.load("./model/model.sav")
        self.array_features = {}
        self.prediction = 0

    # {features = ['bpm', 'ibi', 'rmssd', 'sdnn', 'pnn50']}
    def get_prediction(self):
        """ return the presiction on the array_features """
        self.prediction = self.model.predict(self.array_features)
        return self.prediction

    def construct_array_features(self, bpm, rr_interval, rmssd, sdnn, pnn50):
        """Construct the array of features to make the prediction"""
        self.array_features = {
            "bmp" : bpm,
            "ibi": rr_interval,
            "rmssd": rmssd,
            "sdnn": sdnn,
            "pnn50": pnn50
        }