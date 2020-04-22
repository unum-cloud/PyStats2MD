
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = '0.1.0'

setup(
    name='PyStats2MD',
    version=__version__,
    author='Ashot Vardanian',
    author_email='ashvardanian@gmail.com',
    url='https://github.com/ashvardanian/PyStats2MD',
    description='''

    ''',
    long_description=long_description,
    packages=['pystats2md'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
