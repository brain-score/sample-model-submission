from model_tools.activations.keras import load_images, KerasWrapper
import keras.applications
from test import test_models

# This is an example implementation for submitting resnet50 as a keras model to brain-score
# If you use keras, don't forget to add it and its dependencies to the setup.py


def get_model_list():
    return ['vgg-16']


def get_model(name):
    assert name == 'vgg-16'
    model = keras.applications.vgg16.VGG16()
    model_preprocessing = keras.applications.resnet50.preprocess_input
    load_preprocess = lambda image_filepaths: model_preprocessing(load_images(image_filepaths, image_size=224))
    wrapper = KerasWrapper(model, load_preprocess)
    wrapper.image_size = 224
    return wrapper


def get_layers(name):
    assert name == 'vgg-16'
    return [f'block{i + 1}_pool' for i in range(5)] + ['fc1', 'fc2']


if __name__ == '__main__':
    test_models.test_base_models(__name__)

