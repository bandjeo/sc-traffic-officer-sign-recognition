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

num_features = 20
num_frames_for_train = 300
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
    model.add(LSTM(32,
                   batch_input_shape=(batchSize, num_frames, num_features),
                   return_sequences=True,
                   stateful=stateful))
    model.add(Dropout(0.2))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(total_poses, activation="softmax"))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    print(model.summary())
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
        model.fit(data_x, data_y, epochs=epochs)
    model.save(f"{saved_models_location}{current_date}---videonum_{file_num}.h5")


def generate_starting_frame(poses):
    while True:
        frame_index = random.randrange(len(poses) - num_frames_for_train)
        if poses[frame_index] == 'BEZ_POZE':
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

    # model = create_model(forTraining=False)
    # model.set_weights(modelTraining.get_weights())
    #
    # input_data = np.array([[[1.5432778569374546, 3.3566978985154705, 1.531237434425409, 2.79668232822279,
    #                          1.8373025805784233, 4.703939818764676, 1.7300926787229247, 4.420871060268425,
    #                          0.3922375791715402, 5.548539375350494, 1.1933219208086734, 1.5245880391283286,
    #                          2.315286220828475, 3.1997542796955187, 2.2485330447399123, 3.1260978426601183,
    #                          2.0885611042132655, 3.216404724659048, 2.294673770319466, 3.276863369076928]]])
    # print(model.predict(input_data))
