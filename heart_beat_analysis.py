import numpy as np
import matplotlib.pyplot as plt

TIMESTAMPS_FILE_NAME = "heart_beat_timestamps"
RR_FILE_NAME = "heart_beat_rr"
SESSION_DURATION = 60 # Il vettore timeseries conterrà 60 secondi di samples
MAX_MISSING_SAMPE_FOR_SESSION = 5

class HeartBeatAnalysis: 
    """ Class for the Study of the Heart-beat series """
    def __init__(self):
        self.timeseries = []
        self.rr_intervals = []
        self.missing_samples = 0
    

    # https://github.com/sam-luby/ECG-Pi/blob/master/ecg/pan_tomp.py#L112
    def calculate_bpm(self):
        """ Avendo controllato se ho raggiunto la lunghezza della sessione, mi basta contare quanti sono gli rr-intervals"""
        bpm = len(self.rr_intervals)
        return bpm
    
    def compute_rr_intervals(self):
        """ This function return the differences of every two-consecutive heart-beat-timestamps """
        self.rr_intervals[:] = []   #distrugge il vecchio rrintervals
        for i in range(len(self.timeseries) - 1):
            diff = self.timeseries[i + 1] - self.timeseries[i]
            self.rr_intervals.append(diff)

    def get_session_duration(self):
        """ calcola la durata della sessione di campionamento attuale """
        _sum = sum(self.rr_intervals)
        print("get_session_duration(): " + str(_sum))
        return _sum
    
    def session_duration_reached(self) -> bool :
        """ if the in the session has been sampled "#SESSION_DURATION second-samples", then returns True, else False """
        return ( self.get_session_duration() >= SESSION_DURATION )
    
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
        """ reset(WITHOUT CHANGING THE REFEENCED OBJECTS) the two arrays. You must NOT do -> self.timeseries[] = [] """
        self.timeseries[:] = []
        self.rr_intervals[:] = []

    def write_timeseries(self):
        """ write in .csvFile the timeseries """
        with open(TIMESTAMPS_FILE_NAME + '_' + str(SESSION_DURATION) + '.csv', 'a') as file:
            _len = len(self.timeseries) - 1
            for i, timestamp in enumerate(self.timeseries):
                file.write(str(timestamp) + (',' if i != _len else ''))

    def write_rrintervals(self):
        """ write in .csvFile the rr_intervals """
        with open(RR_FILE_NAME + '_' + str(SESSION_DURATION) + '.csv', 'a') as file:
            _len = len(self.rr_intervals) - 1
            for i, rr_interval in enumerate(self.rr_intervals):
                file.write(str(rr_interval) + (',' if i != _len else ''))

    @staticmethod
    def count_missing_sample(semax_missing_sampleslf, differences : []) :
        return