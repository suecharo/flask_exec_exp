#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path

from setuptools import setup

BASE_DIR: Path = Path(__file__).parent.resolve()
LONG_DESCRIPTION: Path = BASE_DIR.joinpath("README.md")

setup(
    name="flask_exec_exp",
    version="1.0.0",
    description="Flask Executor Experiment",
    long_description=LONG_DESCRIPTION.open(mode="r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="suecharo",
    python_requires=">=3.7",
    platforms="any",
    packages=["flask_exec_exp"],
    install_requires=[
        "flask",
        "flask-executor"
    ],
)
