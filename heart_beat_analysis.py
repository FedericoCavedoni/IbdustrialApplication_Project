import numpy as np
import matplotlib.pyplot as plt

class heart_beat_analysis:

    """ Class for the Study of the Heart-beat series """
    def __init__(self):
        self.timeseries = []
        self.rr_intervals = []
        self.max_missing_samples = 3
        self.timeserires_duration_threshold = 60 # Il vettore timeseries conterrà 60 secondi di samples
        self.missing_samples = 0
    
    def get_timeseries_duration(self, rr_intervals):
        """ calcola la durata della sessione di campionamento attuale """
        _sum = sum(rr_intervals)
        print("get_timeseries_duration: " + str(_sum))
        return _sum

    # https://github.com/sam-luby/ECG-Pi/blob/master/ecg/pan_tomp.py#L112
    def calculate_bpm(self):
        """ Avendo controllato se ho raggiunto la lunghezza della sessione, mi basta contare quanti sono gli rr-intervals"""
        bpm = len(self.rr_intervals)
        return bpm
    
    def compute_rr_intervals(self):
        """ This function return the differences of every two-consecutive heart-beat-timestamps """
        rr_intervals = []
        for i in range(len(self.timeseries) - 1):
            diff = self.timeseries[i + 1] - self.timeseries[i]
            #self.rr_intervals.append(diff)
            rr_intervals.append(diff)
        return rr_intervals
    
    def timeseries_duration_reached(self) -> bool :
        """ if has been sampled at least _THRESHOLD_TIMESERIES samples, returns True, else False """
        return ( len(self.timeseries) == self.timeserires_duration_threshold )
    
    def calculate_RMSSD(self, results):
        """ calculate RMSSD (root mean square of successive differences) """
        RR_list = results['RR_list']
        print(RR_list)
        x = 0
        for i in range(len(RR_list)-1):
            x += (RR_list[i+1] - RR_list[i])**2
        x = x * (1 / (len(RR_list) - 1))
        rmssd = math.sqrt(x)
        print(rmssd)
        return rmssd

    def deastroy_timeseries(self):
        """ resettimano i sample """
        self.timeseries = []
        self.rr_intervals = []

    @staticmethod
    def count_missing_sample(semax_missing_sampleslf, differences : []) :
        return