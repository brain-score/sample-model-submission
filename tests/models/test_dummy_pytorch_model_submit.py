import functools

import torchvision.models
from model_tools.activations.pytorch import PytorchWrapper
from model_tools.activations.pytorch import load_preprocess_images
from model_tools.check_submission import check_models


def get_model_list():
    return ['dummy_model']


def get_model(name):
    assert name == 'dummy_model'
    from torch import nn
    model = nn.Sequential(nn.Conv2d(3, 3, 3)) 
    preprocessing = functools.partial(load_preprocess_images, image_size=224)
    wrapper = PytorchWrapper(identifier='alexnet', model=model, preprocessing=preprocessing)
    wrapper.image_size = 224
    return wrapper


def get_layers(name):
    assert name == 'dummy_model'
    return ['0']


def get_bibtex(model_identifier):
    return """Dummy Model"""


def test_dummy_pytorch_model_submit():
    check_models.check_base_models(__name__)
