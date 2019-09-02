"""main.py"""
from invoke import Collection, Program
#import pkg_resources
from secretctl import cli
from better_setuptools_git_version import get_version
program = Program(namespace=Collection.from_module(cli), version=get_version())
#program = Program(namespace=Collection.from_module(cli), version=pkg_resources.get_distribution('secretctl').version)
