from model_tools.activations.keras import load_images, KerasWrapper
import keras.applications


# This is an example implementation for submitting resnet50 as a tensorflow SLIM model to brain-score
# If you use tensorflow, don't forget to add it and its dependencies to the setup.py
def get_model_list():
    return ['resnet50']


def get_model(name):
    assert name == 'resnet50'
    TFSlimModel.init('resnet-50_v1', net_name='resnet_v1_50', preprocessing_type='vgg',
                     image_size=224, labels_offset=0)
    model = keras.applications.vgg16.VGG16()
    model_preprocessing = keras.applications.resnet50.preprocess_input
    load_preprocess = lambda image_filepaths: model_preprocessing(load_images(image_filepaths, image_size=224))
    wrapper = KerasWrapper(model, load_preprocess)
    wrapper.image_size = 224
    return wrapper


def get_layers(name):
    assert name == 'resnet-50'
    return [f'block{i + 1}_pool' for i in range(5)] + ['fc1', 'fc2']


def get_bibtex(model_identifier):
    return """@article{DBLP:journals/corr/HeZRS15,
              author    = {Kaiming He and
                           Xiangyu Zhang and
                           Shaoqing Ren and
                           Jian Sun},
              title     = {Deep Residual Learning for Image Recognition},
              journal   = {CoRR},
              volume    = {abs/1512.03385},
              year      = {2015},
              url       = {http://arxiv.org/abs/1512.03385},
              archivePrefix = {arXiv},
              eprint    = {1512.03385},
              timestamp = {Wed, 17 Apr 2019 17:23:45 +0200},
              biburl    = {https://dblp.org/rec/journals/corr/HeZRS15.bib},
              bibsource = {dblp computer science bibliography, https://dblp.org}
            }"""