# Part 2: Hydra

## Overview
In this part of the practical, we will use Hydra to configure a simple machine learning experiment.

Hydra is a framework for elegantly configuring complex applications in Python (not just ML research). Hydra constructs a configuration object that is passed to your application using a combination of structured, hierarchical configuration files and command line overrides.

For ML research, where there are often many parameters we may wish to vary, Hydra can be extremely useful to manage this configuration in a structured way. It also works very well with object-oriented frameworks such as PyTorch, allowing you to instantiate the objects e.g. models within your application with minimal boilerplate code.

## Instructions

### 1. Get started.
Create a Conda environment for the project from the adjacent `env/environment.yml` file. From within this directory, check that the script runs with default parameters with:
```bash
python script.py
```
This will train and evaluate an MLP on MNIST using the Adam optimizer.
</br>**Q**: How/where are these defaults being set?

### 2. Implement a new optimiser.
**Task**: Add the ability to use the AdamW optimizer.

See the `config/optimizer/sgd.yaml` file for an example of how existing optimizers are configured.

### 3. Implement a new model.
The `models.py` file contains implementations of a multi-layer perceptron (MLP), fully-convolutional neural network (FCNN) and a Vision Transformer (ViT).

**Task**: Implement a simple linear classifier within `models.py` to serve as a baseline. Once implemented, you should be able to run the model with `python script.py model=linear`.

### 4. Perform a multi-run sweep.
**Task**: Perform a sweep over all combinations of models (linear, MLP, CNN, ViT) and datasets using the AdamW optimizer with a single command.

This can be achieved using the `--multirun` flag:
https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/

### Questions:
- What benefits has Hydra provided us in this example?
- Are there any drawbacks to this approach to configuration over e.g. `argparse`, `click` or using static configuration files?

## Extras
This demo contains only a small subset of Hydra's capabilities. Some other functionalities you might be interested in include:
- Running multi-run sweeps in parallel on a Slurm cluster: https://hydra.cc/docs/plugins/submitit_launcher/
- [Custom callbacks](https://hydra.cc/docs/experimental/callbacks/). For example, to [check you're running on a clean Git branch](https://github.com/paquiteau/hydra-callbacks/blob/e63e82da8d83c6950d272ac34434523077ef6643/src/hydra_callbacks/callbacks.py#L96.).
- Automated parameter optimization e.g. using Ax or Optuna: https://hydra.cc/docs/plugins/ax_sweeper/

![img](https://hydra.cc/img/logo.svg)