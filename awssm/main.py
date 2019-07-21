from invoke import Argument, Collection, Program
from awssm import commands

program = Program(namespace=Collection.from_module(commands), version='0.0.1')
