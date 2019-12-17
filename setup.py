"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path
from itertools import chain
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

extras_require={
    'test': ['coverage', 'pytest'],
    'dev': ['asv'],
}

extras_require['all'] = list(set(chain(*extras_require.values())))

setup(
    name='SocSIM',
    version='0.2.0',
    description='A simulation of self-organized criticality',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/okmechak/SocSIM',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics'
        'License :: BSD 3-clause',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='self-organized-criticality sandpile forest-fire simulation',
    packages=find_packages(exclude=['docs', 'docsrc', 'research', 'resources','results']),
    python_requires='>=3.6',
    install_requires=['numpy', 'matplotlib', 'tqdm', 'numba', 'zarr'],
    extras_require=extras_require,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    project_urls={
        'Bug Reports': 'https://github.com/SocSim/SocSIM/issues',
        'Source': 'https://github.com/SocSim/SocSIM/',
    },
)
