import numpy as np
import matplotlib.pyplot as plt

TIMESTAMPS_FILE_NAME = "heart_beat_timestamps"
RR_FILE_NAME = "heart_beat_rr"
SESSION_DURATION = 60 # Il vettore timeseries conterrà 60 secondi di samples
MAX_MISSING_SAMPE_FOR_SESSION = 5
PROF_TEST = True

class HeartBeatAnalysis:
    """ Class for the Study of the Heart-beat and the computation of the HRV Scores """

    def __init__(self):
        self.timeseries = []
        self.rr_intervals = []
        self.missing_samples = 0
        self.temp_rr_intervals = []

    # https://github.com/sam-luby/ECG-Pi/blob/master/ecg/pan_tomp.py#L112
    def compute_rr_intervals(self):
        """ This function return the differences of every two-consecutive heart-beat-timestamps """
        self.rr_intervals[:] = []   #Empty the older rr_intervals
        for i in range(len(self.timeseries) - 1):
            diff = self.timeseries[i + 1] - self.timeseries[i]
            self.rr_intervals.append(diff)

    def get_average_rrintervals(self):
        """ ritorna la media degli rr_intervals """
        return np.average(self.temp_rr_intervals)

    def get_session_duration(self):
        """ calcola la durata della sessione di campionamento attuale """
        return sum(self.temp_rr_intervals)
    
    def session_duration_reached(self) -> bool :
        """ if the in the session has been sampled "#SESSION_DURATION second-samples", then returns True, else False """
        return ( self.get_session_duration() >= SESSION_DURATION )
    
    def copy__rr_intervals__in__temp_rr_intervals(self):
        """ copy the rr_interval in temp_rr_intervals """
        self.temp_rr_intervals = self.rr_intervals.copy()

    def empty_arrays(self):
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
            _len = len(self.temp_rr_intervals) - 1
            for i, temp_rr_interval in enumerate(self.temp_rr_intervals):
                file.write(str(temp_rr_interval) + (',' if i != _len else '\n'))

    def compute_bpm(self):
        """ return the bmp """
        _session_duration = self.get_session_duration()
        bpm = ( ( _session_duration / self.get_average_rrintervals() )
               *
               ( 60 / _session_duration ) )
        print("bpm(): " + str(bpm))
        if(PROF_TEST):
            with open('statistics.csv', 'a') as file:
                file.write("bpm(): " + str(bpm) + "\n")
        return bpm

    def compute_rmssd(self):
        """ calculate the RootMeanSquareSuccessiveDifferences (root mean square of successive differences) """
        differences = np.diff(self.temp_rr_intervals)
        squared_differences = differences ** 2
        mean_squared_differences = squared_differences / (len(differences) - 1 )
        rmssd = np.sqrt(mean_squared_differences)
        print("compute_rmssd(): " + str(rmssd))
        if(PROF_TEST):
            with open('statistics.csv', 'a') as file:
                file.write("compute_rmssd(): " + str(rmssd) + "\n")
        return rmssd
    
    def compute_standard_deviation(self):
        """ return the Standard Deviation of RR_intervals"""
        sd = np.std(self.temp_rr_intervals)
        print("compute_sdrr(): " + str(sd))
        if(PROF_TEST):
            with open('statistics.csv', 'a') as file:
                file.write("compute_standard_deviation(): " + str(sd) + "\n")
        return sd
    
    def compute_pnn(self, _x_milliseconds = 50):
        """ return the number of successive intervals that distance more than _x millisecond"""
        _len = len(self.temp_rr_intervals)
        NNx = 0
        for i in range(_len - 1):
            if (self.temp_rr_intervals[i + 1] - self.temp_rr_intervals[i]) > _x_milliseconds:
                NNx += 1
        pNNx = NNx / _len
        print("compute_nn(): " + str(NNx) + " Percentage: " + str(pNNx))
        if(PROF_TEST):
            with open('statistics.csv', 'a') as file:
                file.write("compute_nn(): " + str(NNx) + "\n")
                file.write("Percentage(): " + str(pNNx) + "\n")
        return pNNx


    def count_missing_sample(self) :
        print("DA DEFINIRE")
        return