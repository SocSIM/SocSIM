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
[Self-organized criticality wiki](https://en.wikipedia.org/wiki/Self-organized_criticality):
In physics, self-organized criticality (SOC) is a property of __dynamical systems__ that have a __critical point__ as an attractor. Their macroscopic behavior thus displays the spatial or temporal scale-invariance characteristic of the critical point of a phase transition, but without the need to tune control parameters to a precise value, because the system, effectively, tunes itself as it evolves towards criticality.

The concept was put forward by Per Bak, Chao Tang and Kurt Wiesenfeld ("BTW") in a paper published in 1987 in Physical Review Letters, and is considered to be one of the mechanisms by which complexity arises in nature. Its concepts have been enthusiastically applied across fields as diverse as geophysics, physical cosmology, evolutionary biology and ecology, bio-inspired computing and optimization (mathematics), economics, quantum gravity, sociology, solar physics, plasma physics, neurobiology and others.

SOC is typically observed in slowly driven non-equilibrium systems with a large number of degrees of freedom and strongly nonlinear dynamics. Many individual examples have been identified since BTW's original paper, but to date there is no known set of general characteristics that guarantee a system will display SOC.

## 2. Program structure, installation and use cases

### 2.1 Project folder structure
[sources1](https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application)
[source2](https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6)


### 2.2 Installation and dependencies
#### Dependencies
 Probably TensorNetwork, Keras.

### 2.3 Use cases

## 3. Links/References
[1]  Bak, P., Tang, C. and Wiesenfeld, K. (1987). "Self-organized criticality: an explanation of 1/f noise". Physical Review Letters. 59 (4): 381–384. Bibcode:1987PhRvL..59..381B. doi:10.1103/PhysRevLett.59.381. PMID 10035754. Papercore summary: http://papercore.org/Bak1987.
[2] [Abelian sandpile model](https://en.wikipedia.org/wiki/Abelian_sandpile_model)
[3] [Forest-fire model](https://en.wikipedia.org/wiki/Forest-fire_model)
[4] [Theoretical Models of Self-Organized Criticality (SOC) Systems](https://arxiv.org/abs/1204.5119)
[5] [Pink noise](https://en.wikipedia.org/wiki/Pink_noise)
