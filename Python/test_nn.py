import argparse
import pandas as pd
from keras.models import load_model
from train_nn import generate_data, create_model, poses_dtype, poses_names
import numpy as np


dataset_location = "../Node/src/dataset/"
dataset_for_test_location = "../Node/src/dataset/test/output.csv"


def test_training_model(model):
    data = pd.read_csv(dataset_for_test_location, header=None)
    data_x, data_y = generate_data(data)
    result = model.predict(data_x)
    print(model.evaluate(data_x, data_y))
    print(result.shape)
    print(data_x.shape)
    for data_x_batch, data_y_batch, result_batch in zip(data_x[0], data_y[0], result[0]):
        result_pose = poses_names[np.argmax(result_batch)]
        actual_pose = poses_names[np.argmax(data_y_batch)]
        print(f'actual: {actual_pose}  predicted: {result_pose}  scores: {[f"{pn}:{ps}" for pn, ps in zip(poses_names, result[0][0])]}')


def test_model(model):
    data = pd.read_csv(dataset_for_test_location, header=None)
    data_x, data_y = generate_data_all(data)
    for data_x_batch, data_y_batch in zip(data_x, data_y):
        result = model.predict(np.expand_dims(data_x_batch, axis=(0, 1)))
        result_pose = poses_names[np.argmax(result[0][0])]
        actual_pose = poses_names[np.argmax(data_y_batch)]
        print(f'actual: {actual_pose}  predicted: {result_pose}  scores: {[f"{pn}:{ps}" for pn, ps in zip(poses_names, result[0][0])]}')


def generate_data_all(data):
    data_x = data.iloc[:, 1:].to_numpy()
    poses = data.iloc[:, 0:1]
    data_y = pd.get_dummies(poses.astype(poses_dtype), prefix='', prefix_sep='', dtype=np.float).to_numpy()
    return data_x, data_y


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", required=True,
                        help="model to be tested")
    args = parser.parse_args()

    model_training = load_model(args.model)
    model = create_model(forTraining=False)
    model.set_weights(model_training.get_weights())

 #   test_model(model)
    test_training_model(model_training)
