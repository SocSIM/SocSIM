# SocSim
Programs in Python that simulates dynamical systems that have a critical point as an attractor. So called [__self-organized criticality__(SOC)](https://en.wikipedia.org/wiki/Self-organized_criticality)

#### Basic goals of project:
 - Make wide coverage of all self-orfganized cryticality models.
 - Figuring out the best algorithms. 
    - Easy scalling on many processors machine(multithreading, [GPGPU](https://en.wikipedia.org/wiki/General-purpose_computing_on_graphics_processing_units), CUDA). 
    - Optimal memory usage.
    - Applying some commmon libraries(Working with tensors etc.).
 - Using some best practice of programming:
    - [Coding conventions](https://en.wikipedia.org/wiki/Coding_conventions)
    - Unit Tests.
    - Creation of common modules.
    - Automatic documentation generation.
    - Readability of code and easy of use(between clearnes and speed, we should choose clearnes).
 - Input\Output of program. Database of simulations. In other word we should somehow track I/O of program for reproducing or postprocessing of results. And as experience shows it is a 60% of problem. Should we use some databases or immideatly process results and save them in form of posts(like JuPyter or Mathmetica)? Also those "posts" should be on website ot github wiki?
 - How about quantum algorithms?
 - How we can apply [Keras](https://github.com/keras-team/keras)? Predictions, finding hiden parameters, etc.


### 0.1 Ok, some todo's:

In __Basic goals of project__ are some questions and commitment without solutions, so lets list here some priority list:

- [ ] Template of project.
- [ ] Make an research of _SOC_ topic.
- [ ] How basic python project template looks like?
- [ ] Codding conventions in python.
- [ ] Documentation generation in python.
- [ ] How to export/save Jupiter notebooks(to make a posts later)
- [ ] Rest of todo's goals.

### 0.2 Commitments
Here are descibed code formatting style and other conventions, to make code more _uniform_. Also this section is for newcomers and contributors.

#### Code formatting
Consider next two style guides
 - [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md), and
 - [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)(official Python style guide).
 
#### Unit Tests:
Python has built-in library for running tests:
[__unittest__](https://docs.python.org/3/library/unittest.html)

#### Logging
Logging helps to debug application and also is provided by Python standard library
[logging](https://docs.python.org/3.9/library/logging.html)
 
#### Documentation
Most popular documentation generator for Pyhon - [Sphinx](http://www.sphinx-doc.org/en/master/).


## 1. Theoretical problem description
[Self-organized criticality wiki](https://en.wikipedia.org/wiki/Self-organized_criticality)

## 2. Program structure, installation and use cases

### 2.1 Project folder structure
[sources1](https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application)


### 2.2 Installation and dependencies
#### Dependencies
 Probably TensorNetwork, Keras.

### 2.3 Use cases

## 3. Links/References
