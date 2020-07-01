
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = '0.3.0'

setup(
    name='pystats2md',
    version=__version__,
    author='Ashot Vardanian',
    author_email='info@unum.xyz',
    url='https://unum.xyz/pystats2md',
    description='''
        Generate Markdown tables & Plotly charts from Google Benchmark outputs or directly in Python!
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
