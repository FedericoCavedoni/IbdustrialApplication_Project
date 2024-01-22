import os
import wfdb
import numpy as np
import matplotlib.pyplot as plt

class emulator_sensor:

    """Emulator class of ECG sensors """
    def __init__(self, folder_name = "sensor_data"):
        self.data_record_name = ['100','101','102','103','104','105','106','107','108','109','111','112','113','114','115','116','117','118','119','121','122','123','124','200','201','202','203','205','207','208','209','210','212','213','214','215','217','219','220','221','222','223','228','230','231','232','233','234']
        self.data_record_index = 0
        self.folder_name = folder_name
        if os.path.isdir("sensor_data"):
            print('Folder sensor_data found!')
        else:
            print('No data')
    

    def read_sample(self):
        """ legge come array circolare i record e crea il plot (PER ADESSO)"""
        record_name = self.folder_name + self.data_record_name[self.data_record_index]
        record = wfdb.rdsamp(record_name, sampto=3000)
        #annotation = wfdb.rdann(record_name, 'atr', sampto=3000)

        fig, ax = plt.subplots(nrows=2, figsize=(12,6))
        ecg_sensor_1 = record[0][:, 0]
        ecg_sensor_2 = record[0][:, 1]


        ax[0].set_ylabel('ecg_sensor_1')
        ax[1].set_xlabel('Datapoints')
        ax[1].set_ylabel('ecg_sensor_2')

        ax[0].plot(ecg_sensor_1)
        ax[1].plot(ecg_sensor_2)
        record_name = self.data_record_name[self.data_record_index]

        with open(record_name + "_ecg_sensor_1.csv", 'a') as file:
            for valore in ecg_sensor_1:
                file.write(str(valore) + ',')

        with open(record_name + "_ecg_sensor_2.csv", 'a') as file:
            for valore in ecg_sensor_2:
                file.write(str(valore) + ',')

        fig.savefig(record_name + ".png")
        print("Avrei inviato i sample di cui ho creato il {}.png ".format(record_name))
        
        self.data_record_index = (self.data_record_index + 1) % len(self.data_record_name)
        