import pandas as pd
import numpy as np
import heartpy as hp
import math
import joblib
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

annotations_train = ['gamer1-annotations.csv', 'gamer2-annotations.csv', 'gamer3-annotations.csv', 'gamer4-annotations.csv']
ppg_train = ['gamer1-ppg-2000-01-01.csv', 'gamer1-ppg-2000-01-02.csv','gamer2-ppg-2000-01-01.csv', 'gamer2-ppg-2000-01-02.csv','gamer3-ppg-2000-01-01.csv', 'gamer3-ppg-2000-01-02.csv', 'gamer4-ppg-2000-01-01.csv', 'gamer4-ppg-2000-01-02.csv']

# returns dataframe of ppg signal based on filename (file from kaggle input folder)
# removes non-finite values
# moving average filter

def read_ppg(filename):
    df = pd.read_csv('data/' + filename)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.fillna(0)
    df.astype({'Red_Signal': 'int64'}).dtypes
    df.Red_Signal.rolling(50, min_periods=1).mean() # moving average
    return df["Red_Signal"]

# returns dataframe of selected features from the heartpy processing result removing NaN values

def pick_features(all_measures, selected):
    x_train = []
    for i in range(len(all_measures['bpm'])):
        row = []
        for cat in selected:
            value = all_measures[cat][i]
            row.append(remove_nan(value))
        x_train.append(row)
    return x_train

# if value is NaN return 0 else returns value

def remove_nan(value):
    if math.isnan(value):
        return 0
    return value

# filters and processes ppg dataframe with heartpy

def process_ppg(data):
    sr = 100
    filtered = hp.filter_signal(data, [0.5, 15], sample_rate=sr, order=3, filtertype='bandpass')

    working_data, measures = hp.process_segmentwise(filtered, sample_rate=sr, segment_width=40, segment_overlap=0.25, segment_min_size=30)
    return  working_data, measures

def x_data(filename, selected_features):

   data = read_ppg(filename)

   working_data, measures = process_ppg(data)

   return pick_features(measures, selected_features)

def y_data(filename, size):
    data = []
    sleepiness = []
    with open('data/' + filename) as file:
        file.readline()
        for row in file:
            time, event, value = row.strip().split(',', 2)
            if event == 'Stanford Sleepiness Self-Assessment (1-7)':
                value = int(value)
                if value < 4:
                    sleepiness.append(0)
                else:
                    sleepiness.append(1)

    for i in range(len(sleepiness)):
        data = data + [sleepiness[i]] * math.ceil(size/25)

    return data[:size]

def read_gamer(x_file1, x_file2, y_file, features):
    x_result = x_data(x_file1, features)
    x_result = np.concatenate((x_result, x_data(x_file2, features)), axis=0)
    y_result = y_data(y_file, len(x_result))
    return x_result, y_result

"""# Reading data"""

#['bpm', 'ibi', 'sdnn', 'sdsd', 'rmssd', 'pnn20', 'pnn50', 'hr_mad', 'sd1', 'sd2', 's', 'sd1/sd2', 'breathingrate', 'segment_indices']

features = ['bpm', 'ibi', 'rmssd', 'sdnn', 'pnn50']

"""**Training data**"""

x_train = []
y_train = []

for i in range(4):
    x, y = read_gamer(ppg_train[i*2], ppg_train[i*2+1], annotations_train[i], features)

    for line in x:
        x_train.append(line)
    y_train = y_train + y

"""**Test data**"""

x_test, y_test = read_gamer('gamer5-ppg-2000-01-01.csv', 'gamer5-ppg-2000-01-02.csv', 'gamer5-annotations.csv', features)

model = KNeighborsClassifier(n_neighbors=20).fit(x_train, y_train)

prediction = model.predict(x_test)

recall = recall_score(y_test, prediction)
precision = precision_score(y_test, prediction)
acc = accuracy_score(y_test, prediction)
f1 = f1_score(y_test, prediction)
dati = {'model': 'KNN', 'accuracy': acc, 'precision' : precision, 'recall' : recall, 'f1-score' : f1}

print(dati)

joblib.dump(model, 'model/model.joblib')

model = joblib.load('model/model.joblib')

index = random.randint(0, len(x_test) - 1) -1
record = x_test[index:index+1,]

prediction = model.predict(record)

print(prediction)
