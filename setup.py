#!/usr/bin/env python36
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="php_whisperer",
    version="3.0.0",
    author="Matthew Nicol",
    author_email="matthew.b.nicol@gmail.com",
    description="Read and write php arrays with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'whisperer_read_stdin = php_whisperer.read_php:read_php_stdin',
        ]
    },
    url="https://github.com/matthewnicol/php_whisperer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)


