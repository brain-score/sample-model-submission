
#Brainscore submission template
This is the template module, to add your neural network implementation and submit it to brain-score. It provides examples and template methods for an easy submission.

##Getting started
To submit a model to brain-score, the source code has to be submitted as a zip file. The framework will unpack und install the code and its dependencies in a sandboxed environment and execute the brain-score benchmarks on it.
One submission can contain multiple models. Once all models are scored on the benchmarks, an email with the results is sent to the submittor. The results will *NOT* be published somewhere without explicit approval of the repository owner.
Additionally the submitted content will not be accessible to any other than the automated benchmark framework, no human will see the implementations.

### Setup
There are two options to set up the submission: Either clone this repository and add a neural network implementation here, or add the required submission modules to an existing repository.
####Setup this repository
The submission can contain multiple models. To create a submission do following steps:
  1. Clone this repository and rename it.
  2. Install the repositories dependencies by executing `pip install .` in the projects root directory(maybe also in a virtual environment)
  3. Add model implementations to the corresponding file(`base_model.py` or `brain_model.py`). The methods are well commented and describe what to add and return. There are some example base model implementations provided for common machine learning libraries in the examples folder.
  4. Add *ALL* required libraries to the setup.py. If some dependencies are missing, the scoring mechanism will fail.
  5. Run a test run, to see if the scoring mechanism works, by executing the main method in the template module. It will run a mock run of the benchmark process. The test will run a while, because it does the layer to brain region mapping using cross validation.
  
#### Add modules to existing project
As a second way you can add the required modules to an existing project. Therefore copy the folders "models and test" to the existing project. Make sure to add all the dependencies listed in setup.py to the other project. You can check if your submission is correct, by executing the main method of the modules in `models` directory.

### What kind of model do I submit?
Brain-score accepts two kind of models. The first type are base models, which are classic neural networks with layers, which procude activations. The other alternative are actual brain-models, which take a set of stimulis as input and produce neurid values per stimuli.
If you choose to submit a base model, the models layers will internaly be mapped to brain regions and the models activations will be used to predict brain activities, which then are used as brain model.
Depending on your choice you will have to implement either the `base_model.py` or `brain_model.py` module. But most likely the base model will be the right choice for normal artificial neural networks.

###Base models
We provide several base model implementations in examples folder. The examples work with wrapper classes imported from a [model-tools](https://github.com/brain-score/model-tools) project. 
There are more wrapper implementations avaiable in [activations](https://github.com/brain-score/model-tools/tree/master/model_tools/activations) folder. For further understanding of how the benchmarking works checkout this [jupyter notebook](https://github.com/brain-score/candidate_models/blob/master/examples/score-model.ipynb).
It is located in a repository, containing previously submitted model implementations. This is also a good project to see further examples.

###Brain models
To implement a brain model, the instance has to implement the [BrianModel interface](https://github.com/brain-score/brain-score/blob/master/brainscore/model_interface.py). An example of how to do that can be seen in this [jupyter notebook](https://github.com/brain-score/brain-score/blob/master/examples/benchmarks.ipynb).
  
  
###Create zip and submit   
Once you're confiden your implementation works and the test run returns successful, you can submit the project by creating a zip file. The file has to contain the projects root directory as a single entry.
Go to the [brain-score](http://www.brain-score.org/) website, register and submit your model. Once the results are calculated, you will get an email. Attention: Depending on how many models you have specified in one submission, the process will take a while. Please do not submit more than 3 models at a time!

### Further documentation sources
The brain-score projects are open source and can be freely explored.

Important projects to have a look at could be:
 - The [brain-score](https://github.com/brain-score/brain-score) project itself, which contains the benchmarking code plus a small set of locally executable benchmarks.
 - The [candidate_models](https://github.com/brain-score/model-tools) project contains model implementations, implemented by Dicarlo lab and other contributers. This is a good project to explore how the model intergration is done. 
 - The [model-tools](https://github.com/brain-score/candidate_models) This project contains useful helper methods for adding new base models.