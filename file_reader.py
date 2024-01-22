import os
import wfdb
import numpy as np
import matplotlib.pyplot as plt

class file_reader:
    def __init__(self, path) -> None:
        pass
    

if os.path.isdir("sensor_data"):
    print('You already have the data.')
else:
    print('No data')

record = wfdb.rdsamp('sensor_data/100', sampto=3000)
annotation = wfdb.rdann('sensor_data/100', 'atr', sampto=3000)

fig, ax = plt.subplots(nrows=2, figsize=(12,6))
I = record[0][:, 0]
II = record[0][:, 1]


ax[0].set_ylabel('Lead II')
ax[1].set_xlabel('Datapoints')
ax[1].set_ylabel('Lead II')

ax[0].plot(I)
ax[1].plot(II)

with open("Y.csv", 'a') as file:
    for valore in II:
        file.write(str(valore) + ',')

with open("X.csv", 'a') as file:
    for valore in I:
        file.write(str(valore) + ',')


fig.savefig("fig.png")

print(I)

input()