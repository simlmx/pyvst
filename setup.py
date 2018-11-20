#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pyvst',
    version='0.4.0',
    description='VST2.4 python wrapping using ctypes',
    author='Simon Lemieux',
    author_email='lemieux.simon (at) gmail (dot) (you know what)',
    url='https://github.com/simlmx/pyvst',
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'numpy>=1.15.1',
        'wurlitzer==1.0.1',
    ],
    extras_require={
        'dev': [
            'pytest>=3.8.0',
            'matplotlib>=3.0.0',
            'jupyter>=1.0.0',
        ],
    }
)
