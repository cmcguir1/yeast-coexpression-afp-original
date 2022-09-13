from distutils.command.build import build
from setuptools import setup
from Cython.Build import cythonize

setup (
    ext_modules = cythonize("src/PairwiseYeastNetwork/SpeedTest.pyx")
)