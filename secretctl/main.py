"""main.py"""
from invoke import Collection, Program
from setuptools_scm import get_version
from secretctl import cli

program = Program(namespace=Collection.from_module(cli), version=get_version(root='..', relative_to=__file__))
