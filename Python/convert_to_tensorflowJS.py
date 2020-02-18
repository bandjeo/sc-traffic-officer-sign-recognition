import argparse
from keras.models import load_model
from train_nn import create_model
import tensorflowjs as tfjs


def convert_model(model, output):
    tfjs.converters.save_keras_model(model, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", required=True,
                        help="model to be converted")
    parser.add_argument("-nt", "--not-for-training", action="store_true",
                        help="model is for training")
    parser.add_argument("-o", "--output", default='../AngularApp/src/assets/',
                        help="output dir")
    args = parser.parse_args()

    model = load_model(args.model)
    if not args.not_for_training:
        model_not_training = create_model(forTraining=False)
        model_not_training.set_weights(model.get_weights())
        model = model_not_training

    convert_model(model, args.output)

