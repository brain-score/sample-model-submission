import torch
from model_tools.check_submission import check_models
import functools
from model_tools.activations.pytorch import load_preprocess_images
from model_tools.activations.onnx import OnnxWrapper, get_final_model
import warnings
warnings.filterwarnings("ignore")


"""
Template module for a base model submission to brain-score
"""


def get_model_list():
    """
    This method defines all submitted model names. It returns a list of model names.
    The name is then used in the get_model method to fetch the actual model instance.
    If the submission contains only one model, return a one item list.
    :return: a list of model string names
    """
    return ['resnet18']


def process_model():
    """
    This method returns a list of string layer names to consider per model. The benchmarks maps brain regions to
    layers and uses this list as a set of possible layers. The lists doesn't have to contain all layers, the less the
    faster the benchmark process works. Additionally the given layers have to produce an activations vector of at least
    size 25! The layer names are delivered back to the model instance and have to be resolved in there. For a pytorch
    model, the layer name are for instance dot concatenated per module, e.g. "features.2".
    :param name: the name of the model, to return the layers for
    :return: a list of strings containing all layers, that should be considered as brain area.
    """

    # Pytorch Testing:
    models = ["alexnet", "densenet161", "resnet18", "vgg16", "squeezenet1_1", "resnet152"]
    model_to_choose = models[0]
    model = torch.hub.load('pytorch/vision:v0.10.0', model_to_choose, pretrained=True)
    name = model_to_choose

    # # ONNX Testing:
    # model = onnx.load("googlenet-3.onnx")
    # onnx.checker.check_model(model)
    # name = "googlenet-3"

    # can be either 'onnx' or 'pytorch'. If pytorch model, we will convert to ONNX for you.
    framework = 'pytorch'

    # define these hyperparameters for your model
    input_image_size = 224
    batch_size = 10
    in_channels = 3  # For color images, in_channels = 3. For grayscale, it is 1.

    # convert model from pytorch to ONNX
    onnx_model, layers = get_final_model(framework, batch_size, in_channels, input_image_size, model, name)
    print(f"All Model Layers:\n{layers}")

    # you can return all layers, or just a few with the layers list. Default is the first layer only:
    layers = layers[0:2]
    print(f"Selected Model Layers:\n{layers}")

    # Standard Brain-Score Processing
    preprocessing = functools.partial(load_preprocess_images, image_size=input_image_size)
    wrapper = OnnxWrapper(identifier=name, model=onnx_model, preprocessing=preprocessing)
    wrapper.image_size = input_image_size

    return wrapper, layers


def get_bibtex(model_identifier):
    """
    A method returning the bibtex reference of the requested model as a string.
    """

    return """@incollection{NIPS2012_4824,
                  title = {ImageNet Classification with Deep Convolutional Neural Networks},
                  author = {Alex Krizhevsky and Sutskever, Ilya and Hinton, Geoffrey E},
                  booktitle = {Advances in Neural Information Processing Systems 25},
                  editor = {F. Pereira and C. J. C. Burges and L. Bottou and K. Q. Weinberger},
                  pages = {1097--1105},
                  year = {2012},
                  publisher = {Curran Associates, Inc.},
                  url = {http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf}
                  }"""


if __name__ == '__main__':
    # Use this method to ensure the correctness of the BaseModel implementations.
    # It executes a mock run of brain-score benchmarks.
    check_models.check_base_models(__name__)
