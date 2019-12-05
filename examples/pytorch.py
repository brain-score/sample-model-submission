import functools

import torchvision.models
from model_tools.activations.pytorch import PytorchWrapper
from model_tools.activations.pytorch import load_preprocess_images

from test import test_models


# This is an example implementation for submitting alexnet as a pytorch model
# If you use pytorch, don't forget to add it to the setup.py


def get_model_list():
    return ['alexnet']


def get_model(name):
    assert name == 'alexnet'
    model = torchvision.models.alexnet(pretrained=True)
    preprocessing = functools.partial(load_preprocess_images, image_size=224)
    wrapper = PytorchWrapper(identifier='alexnet', model=model, preprocessing=preprocessing)
    wrapper.image_size = 224
    return wrapper


def get_layers(name):
    assert name == 'alexnet'
    return ['features.2', 'features.5', 'features.7', 'features.9', 'features.12',
            'classifier.2', 'classifier.5']


if __name__ == '__main__':
    test_models.test_base_models(__name__)
