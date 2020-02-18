from __future__ import print_function
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Dropout
import numpy as np
import pandas as pd
import argparse
import random
from sklearn.preprocessing import OneHotEncoder
import os
from datetime import datetime

dataset_location = "../Node/src/dataset/"
saved_models_location = "savedModels/"

num_frames_for_train = 900
num_features = 20
poses_names = ['BEZ_POZE', 'DIGNUTA_RUKA', 'ISPRUZENA_RUKA_1', 'ISPRUZENA_RUKA_2', 'ISPRUZENA_RUKA_3',
               'ISPRUZENA_RUKA_4', 'POVECAJ_BRZINU', 'PRIDJI_BLIZE', 'SMANJI_BRZINU', 'STAJACA_POZA_1',
               'STAJACA_POZA_2', 'ZAUSTAVI_VOZILO']
total_poses = 12
enc = OneHotEncoder(categories=poses_names)
poses_dtype = pd.api.types.CategoricalDtype(categories=poses_names)

current_date = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')


def create_model(forTraining=True):
    if forTraining == True:
        batchSize = None
        num_frames = num_frames_for_train
        stateful = False

    else:
        batchSize = 1
        num_frames = 1
        stateful = True

    model = Sequential()
    model.add(LSTM(256,
                   batch_input_shape=(batchSize, num_frames, num_features),
                   return_sequences=True,
                   stateful=stateful))
    model.add(Dropout(0.3))
    # model.add(LSTM(32,
    #                return_sequences=True,
    #                stateful=stateful))
    # model.add(Dropout(0.3))
    # model.add(LSTM(32,
    #                return_sequences=True,
    #                stateful=stateful))
    # model.add(Dropout(0.3))
    # model.add(Dense(256))
    # model.add(Dropout(0.3))
    model.add(Dense(total_poses, activation="softmax"))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    model.summary()
    return model


def train_model(model, fileNum, epochs, trains_per_file):
    if (fileNum):
        train_on_file(model, fileNum, epochs, trains_per_file)
    else:
        for name in os.listdir(dataset_location):
            if name.isdigit():
                train_on_file(model, name, epochs, trains_per_file)


def train_on_file(model, file_num, epochs, trains_per_file):
    data = pd.read_csv(f"{dataset_location}{file_num}/output.csv", header=None)
    for i in range(trains_per_file):
        data_x, data_y = generate_data(data)
        model.fit(data_x, data_y, epochs=epochs, verbose=0)
        print(f'File: {file_num} Train: {i+1}/{trains_per_file}')
    model.save(f"{saved_models_location}{current_date}---videonum_{file_num}.h5")


def generate_starting_frame(poses):
    while True:
        frame_index = random.randrange(len(poses) - num_frames_for_train)
       # if poses[frame_index] == 'BEZ_POZE':
        return frame_index


def generate_data(data):
    starting_frame_index = generate_starting_frame(data[0])
    data_x = data.iloc[starting_frame_index:starting_frame_index + num_frames_for_train, 1:].to_numpy()
    data_x = np.expand_dims(data_x, axis=0)
    poses = data.iloc[starting_frame_index:starting_frame_index + num_frames_for_train, 0:1]
    data_y = pd.get_dummies(poses.astype(poses_dtype), prefix='', prefix_sep='', dtype=np.float).to_numpy()
    data_y = np.expand_dims(data_y, axis=0)
    return data_x, data_y


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--fileNum",
                        help="train on file number")
    parser.add_argument("-m", "--model",
                        help="continue training of a model")
    parser.add_argument("-e", "--epochs", type=int, default=100,
                        help="epochs per for one training batch")
    parser.add_argument("-t", "--trains-per-file", type=int, default=100,
                        help="number of trains per video file")
    parser.add_argument("-r", "--repeat", action="store_true",
                        help="repeat training until stopped")
    args = parser.parse_args()

    if(args.model):
        model_training = load_model(args.model)
    else:
        model_training = create_model()

    while True:
        current_date = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
        train_model(model_training, args.fileNum, args.epochs, args.trains_per_file)
        if not args.repeat:
            break