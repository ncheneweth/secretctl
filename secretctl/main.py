"""main.py"""
from invoke import Collection, Program
from better_setuptools_git_version import get_version
from secretctl import cli

program = Program(namespace=Collection.from_module(cli), version=get_version().replace('+dirty', ''))
#program = Program(namespace=Collection.from_module(cli), version='0.0.15')
