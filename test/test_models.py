import os

import numpy as np

from brainio_base.assemblies import NeuroidAssembly
from brainio_base.stimuli import StimulusSet
from brainscore.benchmarks import BenchmarkBase
from brainscore.metrics import Score
from brainscore.model_interface import BrainModel
from model_tools.brain_transformation import ModelCommitment


def test_brain_model(module):
    module = __import__(module)
    # func = getattr(module, 'get_model_list')
    # func()
    for model in module.get_model_list():
        layers = module.get_layers(model)
        assert layers is not None
        assert isinstance(layers, list)
        assert len(layers) > 0
        model =module.get_model(model)
        assert model is not None
        assert isinstance(model, BrainModel)
        test_brain_model_processing(model, module)

def test_brain_model_processing(model, module):
    # to be done
    return

def test_base_models(module):
    module = __import__(module)
    for model in module.get_model_list():
        layers = module.get_layers(model)
        assert layers is not None
        assert isinstance(layers, list)
        assert len(layers) > 0
        assert module.get_model(model) is not None
        test_processing(model, module)
        print('Test successful, you are ready to submit!')


def test_processing(model, module):
    os.environ['RESULTCACHING_DISABLE'] = '1'
    model_instance = module.get_model(model)
    layers = module.get_layers(model)
    brain_model = ModelCommitment(identifier=model, activations_model=model_instance,
                                  layers=layers)
    brain_model.commit_region('IT', get_assambly())
    benchmark = MockBenchmark()
    score = benchmark(brain_model)
    assert score is not None
    assert score.sel(aggregation='center')


class MockBenchmark(BenchmarkBase):
    def __init__(self):
        ceiling = Score([1, np.nan], coords={'aggregation': ['center', 'error']}, dims=['aggregation'])
        super(MockBenchmark, self).__init__(
            identifier='mockBenchmark',
            ceiling_func=lambda: ceiling)

    def __call__(self, candidate: BrainModel):
        image_names = ['grayscale.png', 'grayscale2.jpg', 'grayscale_alpha.png']
        stimulus_set = StimulusSet([{'image_id': image_name, 'image_label': image_name[::-1]}
                                    for image_name in image_names])
        stimulus_set.image_paths = {image_name: os.path.join(os.path.dirname(__file__), image_name)
                                    for image_name in image_names}
        stimulus_set.name = 'test'
        # Do brain region task
        candidate.start_recording('IT', [(70, 170)])
        activations = candidate.look_at(stimulus_set)
        # Do behavior task
        behaviour = candidate.start_task(BrainModel.Task.probabilities, stimulus_set)
        propabilites = candidate.look_at(stimulus_set)
        return Score([1, np.nan], coords={'aggregation': ['center', 'error']}, dims=['aggregation'])


def get_assambly():
    assembly = NeuroidAssembly((np.arange(8 * 5) + np.random.standard_normal(8 * 5)).reshape((5, 8, 1)),
                               coords={'image_id': (
                                   'presentation',
                                   ['rgb.jpg', 'grayscale.png', 'grayscale2.jpg', 'grayscale_alpha.png'] * 2),
                                   'object_name': ('presentation', ['a'] * 8),
                                   'repetition': ('presentation', [1, 1, 1, 1, 2, 2, 2, 2]),
                                   'neuroid_id': ('neuroid', np.arange(5)),
                                   'region': ('neuroid', ['IT'] * 5),
                                   'time_bin_start': ('time_bin', [70]),
                                   'time_bin_end': ('time_bin', [170])
                               },
                               dims=['neuroid', 'presentation', 'time_bin'])
    image_names = ['rgb.jpg', 'grayscale.png', 'grayscale2.jpg', 'grayscale_alpha.png']
    object_names = ['a'] * 4
    stimulus_set = StimulusSet([{'image_id': image_names[i], 'object_name': 'a', 'image_label': 'b'}
                                for i in range(4)])
    stimulus_set.image_paths = {image_name: os.path.join(os.path.dirname(__file__), image_name)
                                for image_name in image_names}
    stimulus_set.name = 'test'
    assembly.attrs['stimulus_set'] = stimulus_set
    assembly.attrs['stimulus_set_name'] = stimulus_set.name
    assembly = assembly.squeeze("time_bin")
    return assembly.transpose('presentation', 'neuroid')
