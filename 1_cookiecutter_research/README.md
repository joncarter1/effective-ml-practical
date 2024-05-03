# Part 1: Cookiecutter Research
![img](https://raw.githubusercontent.com/cookiecutter/cookiecutter/3ac078356adf5a1a72042dfe72ebfa4a9cd5ef38/logo/cookiecutter_medium.png)
<sub><sup></br>https://github.com/cookiecutter/cookiecutter</sup></sub>
## Overview
Writing clean, high quality code improves longevity, reproducibility and collaboration.</br>
The purpose of this exercise is to gain exposure to some Python development best practices and common development tools such as [ruff](https://docs.astral.sh/ruff).

Setting up a Python project typically involves a lot of boilerplate code and configuration files: `setup.cfg`, `pyproject.toml`, `requirements.txt` etc. Your time is precious, and as little as possible should be spent writing these files.

In this part of the practical, we will use a tool called `cookiecutter` to auto-generate new ML research repositories from a template. We will look at how this enables us to automate away lots of the configuration involved in Python packaging, including code formatting, linting and testing, allowing you to focus on the bits that you care about i.e. the research.

## Instructions

### 1. Install cookiecutter.
Follow the instructions [here](https://cookiecutter.readthedocs.io/en/stable/installation.html) to install the `cookiecutter` Python package.

(If you use `conda`, it often makes sense to install this into your `base` environment.)

### 2. Generate a cookiecutter repository.
To create a new cookiecutter Git repository from the template, `cd` to the directory you usually store your code repositories in (e.g. `cd $HOME/code`) and run:
```bash
cookiecutter https://github.com/joncarter1/cookiecutter_research.git  --checkout deliberate-bugs
```
This will initiate a dialog, enabling you to configure a number of options for the new repository, such as your name, the name of the new project, and the version of Python to use. After entering these options, a new Git repository will be generated within your current directory. The name of the project folder is set by the value of `project_slug` entered during the dialog. (Note, I'd recommend keeping the `mypy` option set to False).

This cookiecutter template combines some useful features specific to Python software development, with some useful ML research tools (e.g. Hydra). It deliberately contains bugs, which have been introduced to highlight some of the useful features such as automatically configuring code linting, formatting and testing.</br>

More information can be found in the README of the template repository here:
https://github.com/joncarter1/cookiecutter_research
</br>The responsibility of individual files and the meaning of configuration options are also provided as in-line annotations for many of the files within the newly generated repository.

### 3. Install a dedicated Conda environment for the repository.
Separate to your base Conda environment, it typically makes sense to keep separate Conda environments for different projects, to avoid dependency conflicts.

The generated project contains an `environment.yaml` file that you can use to store the dependencies for the project. To install the environment and the adjacent Python package within the project in editable mode, run:
```bash
conda env create --file envs/environment.yaml
conda activate {{ project_slug }} # Replace with name of generated environment
pip install -e .
pre-commit install
```

Installing your research code as a Python package means that you can import the code from anywhere, e.g. within the notebooks or scripts folder, without having to worry about relative import locations, or modifying the Python path.

The `-e` flag means that the imported package stays up-to-date with the local code within the `src` folder.
See e.g. [here](https://stackoverflow.com/questions/35064426/when-would-the-e-editable-option-be-useful-with-pip-install) for more information about editable installs and [here](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) for why a `src` layout is useful.

`pre-commit install` sets up a tool called `pre-commit`, which automatically runs a number of checks on your code whenever you run `git commit`. If these checks fail, the `git commit` is aborted.

These checks are configured by the `.pre-commit-config.yaml` file in the repository. The checks run include:
- Checking for large files.
- Auto-formatting your code.
- Linting your code, including checking for Python style-guide (PEP 8) compliance, and security issues e.g. hard-coded API keys.

It's possible to create your own custom pre-commit checks, and there are a wide range of community extensions. For more info see: https://pre-commit.com/

It's possible to skip the pre-commit hook by running `git commit` with the `--no-verify` flag. You can also manually run the pre-commit checks any time by running `pre-commit run --all-files` from the project root.

### 4. Fix the repository.
### a. Formatting, linting and static errors
**Task:** Fix the pre-commit items.

The generated repository contains a script with a number of static errors and PEP8 violations.

If you run:
```bash
git add *  .editorconfig .gitignore .pre-commit-config.yaml
git commit -m "Initial commit"
```
`pre-commit` will fix some of these errors automatically, and instruct you on how to fix the rest. Unless you explicitly use the `--no-verify` option, `pre-commit` won't commit your code until all of these checks pass. (Hint: See the [dotenv](https://pypi.org/project/python-dotenv/#getting-started) library for an alternative to the insecure `load_dotenv` function).

To re-run the checks, remember to stage your new edits with `git add` then run `git commit` again. This may take a few attempts to fix them all.

### b. Testing
Next, run `pytest` from the root of the repository. This will run the tests implemented within the `tests` folder. This will automatically generate statistics such as the proportion of code within your package covered by the tests i.e. the test coverage.

In the `utils.py` file, there is a function called `patchify_images` that will fail its associated tests. This function is supposed to reshape input images into the input shape used by a Vision Transformer (ViT) model. However, it was generated by [Github Copilot](https://github.com/features/copilot) and isn't quite right.

**Task**: Fix the function implementation so that the associated unit tests pass.

The goal here is not to test your tensor manipulation skills, but to illustrate how we can write simple tests for custom tensor operations. Feel free to find a correct implementation online e.g. from [einops](https://github.com/arogozhnikov/einops) to insert.

<sub><sup>n.b. this simple test case comes from (painful) personal experience, where I nearly completely dropped a (good) idea because an iffy `torch.reshape` operation was causing a silent bug in my code.</sup></sub>

### 5. Run the example script using Hydra.
Once you've fixed the repository, including the unit tests, the script within the `scripts` directory should run with e.g.:
```python
python example.py input_val=3
```
This script uses Hydra to create the input configuration (`cfg`) for the application, by combining the configuration files from the adjacent `config` directory with command-line arguments.

It also simplifies configuration of the Python logging library. Try running with e.g.:
```bash
python example.py hydra.verbose=True
```
to print debug statements to the console.

More advanced usage of Hydra is the focus of the next section of the practical.

### 6. Wrap-up
In this part of the practical we've automated the creation of a Python research repository using cookiecutter, including the creation of environment files, a Python package structure, and code quality checks using `pre-commit`.

Before moving on, I'd recommend making sure you understand what the following libraries do within the codebase:
- `beartype`
- `ruff`

and would highly recommend incorporating them into your own projects.
</br><sub><sup>
Sidenote: The [beartype](https://github.com/beartype/beartype) documentation and Github issues are one of the greatest collections of modern day literature.</sup></sub>

### (Optional) Static type-checking with mypy
Re-generate and re-install the repository with the `mypy` cookiecutter option set to 'y' and re-fix the `pre-commit` checks.

This will enable static type checking of your Python code during the `pre-commit`. Amongst other things, this will check that your type hints are compatible throughout the repository.

For example, if somewhere in your codebase you define:
```python
def func(x: int) -> str:
    return x + 1
```
`mypy` will throw an error during the `pre-commit` because the annotated return type does not match the expected return type for the given input (`int`). `mypy` *can* be useful to improve the quality of your Python code, by spotting errors before any code is run. However, it can also be a bit of a pain when working with numerical libraries (`numpy`, `pandas`, `pytorch` etc.), where type definitions can be flaky.

Ultimately, whether or not to use mypy, or indeed any of the tools introduced in this part of the practical will come down to a trade-off between speed of iteration and code longevity. Though, using tools like cookiecutter, hopefully this example has shown that these two objectives need not be strongly conflicting.