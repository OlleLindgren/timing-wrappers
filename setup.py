"""Installer for timing-wrappers"""
from pathlib import Path
import setuptools

with open(Path(__file__).parent / "README.md", "r", encoding="utf-8") as stream:
    long_description = stream.read()

with open(Path(__file__).parent / "requirements.txt", "r", encoding="utf-8") as stream:
    requirements = list(stream.readlines())

setuptools.setup(
    name="timing-wrappers",
    version="v0.0.2",
    author="Olle Lindgren",
    author_email="lindgrenolle@live.se",
    description="My version of a timing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OlleLindgren/timing-wrappers",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
