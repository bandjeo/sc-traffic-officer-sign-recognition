import argparse
import statistics

import pandas as pd
from keras.models import load_model
from train_nn import generate_data, create_model, poses_dtype, poses_names
import numpy as np

dataset_location = "../Node/src/dataset/"
dataset_for_test_location = "../Node/src/dataset/test/output.csv"


def test_training_model(model):
    data = pd.read_csv(dataset_for_test_location, header=None)
    data_x, data_y = generate_data(data)
    predictions = model.predict(data_x)
    generateResultStatistics(data_x[0], data_y[0], predictions[0])
    # for data_x_batch, data_y_batch, result_batch in zip(data_x[0], data_y[0], result[0]):
    #     result_pose = poses_names[np.argmax(result_batch)]
    #     actual_pose = poses_names[np.argmax(data_y_batch)]
    #     print(f'actual: {actual_pose}  predicted: {result_pose}  scores: {[f"{pn}:{ps}" for pn, ps in zip(poses_names, result_batch)]}')


def test_model(model):
    data = pd.read_csv(dataset_for_test_location, header=None)
    data_x, data_y = generate_data_all(data)
    predictions = []
    for data_x_batch, data_y_batch in zip(data_x, data_y):
        predictions.append(model.predict(np.expand_dims(data_x_batch, axis=(0, 1)))[0][0])
    generateResultStatistics(data_x, data_y, predictions)
    # result_pose = poses_names[np.argmax(result[0][0])]
    # actual_pose = poses_names[np.argmax(data_y_batch)]
    # print(f'actual: {actual_pose}  predicted: {result_pose}  scores: {[f"{pn}:{ps}" for pn, ps in zip(poses_names, result[0][0])]}')


def generate_data_all(data):
    data_x = data.iloc[:, 1:].to_numpy()
    poses = data.iloc[:, 0:1]
    data_y = pd.get_dummies(poses.astype(poses_dtype), prefix='', prefix_sep='', dtype=np.float).to_numpy()
    return data_x, data_y


def generateResultStatistics(data_x, data_y, predictions):
    pose_stats = {pose: {pose: 0 for pose in poses_names} for pose in poses_names}
    pose_averages = {pose: {pose: 0 for pose in poses_names} for pose in poses_names}
    for x, y, prediction in zip(data_x, data_y, predictions):
        prediction_pose = poses_names[np.argmax(prediction)]
        actual_pose = poses_names[np.argmax(y)]
        pose_stats[actual_pose][prediction_pose] += 1
        for i in range(len(poses_names)):
            pose_averages[actual_pose][poses_names[i]] += prediction[i] * 100
    for pose in pose_averages:
        pose_occurrence_num = sum(pose_stats[pose].values()) or 1
        for key in pose_averages[pose]:
            pose_averages[pose][key] = pose_averages[pose][key] / pose_occurrence_num
    pose_recall = {pose: pose_stats[pose][pose] / (sum(pose_stats[pose].values()) or 1) for pose in poses_names}
    pose_precision = {pose: pose_stats[pose][pose] / (sum(val[pose] for val in pose_stats.values()) or 1) for pose in
                      poses_names}
    pose_error_rate = sum([pose_stats[pose][pose] for pose in poses_names]) / len(predictions)
    pose_fvalue = {
        pose: 2 * pose_precision[pose] * pose_recall[pose] / ((pose_precision[pose] + pose_recall[pose]) or 1) for pose
        in poses_names}
    fvalue_macro = statistics.mean(pose_fvalue.values())

    format_string = "{:20}|{:>10}|{:>12}|{:>16}|{:>16}|{:>16}|{:>16}|{:>15}|{:>12}|{:>13}|{:>14}|{:>14}|{:>15}"
    format_string2 = "{:>10}|{:>12}|{:>16}|{:>16}|{:>16}|{:>16}|{:>15}|{:>12}|{:>13}|{:>14}|{:>14}|{:>15}"

    print("{:^200}".format(f"{color.BOLD}CONFUSION MATRIX{color.END}"))
    print(format_string.format('ACTUAL/PREDICTION', *poses_names))
    for key, value in pose_stats.items():
        print(format_string.format(key, *[value[pose] for pose in poses_names]))

    print("\n")

    print("{:^200}".format(f"{color.BOLD}AVERAGE VALUES{color.END}"))
    print(format_string.format('ACTUAL/PREDICTION', *poses_names))
    for key, value in pose_averages.items():
        print(format_string.format(key, *[f'{round(value[pose], 4)}%' for pose in poses_names]))

    print("\n")

    print("{:^200}".format(f"{color.BOLD}POSE RECALL{color.END}"))
    print(format_string2.format(*poses_names))
    print(format_string2.format(*[round(pose_recall[pose], 4) for pose in poses_names]))

    print("\n")

    print("{:^200}".format(f"{color.BOLD}POSE PRECISION{color.END}"))
    print(format_string2.format(*poses_names))
    print(format_string2.format(*[round(pose_precision[pose], 4) for pose in poses_names]))

    print("\n")

    print("{:^200}".format(f"{color.BOLD}POSE F-VALUE{color.END}"))
    print(format_string2.format(*poses_names))
    print(format_string2.format(*[round(pose_fvalue[pose], 4) for pose in poses_names]))

    print("\n")

    print("{:^200}".format(f"{color.BOLD}MACRO F-VALUE:{fvalue_macro}{color.END}"))

    print("\n")

    print("{:^200}".format(f"{color.BOLD}ERROR RATE:{pose_error_rate}{color.END}"))


# printing colors
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", required=True,
                        help="model to be tested")
    args = parser.parse_args()

    model_training = load_model(args.model)
    model = create_model(forTraining=False)
    model.set_weights(model_training.get_weights())

    test_model(model)
#   test_training_model(model_training)
