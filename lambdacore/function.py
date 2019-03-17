'''
    Defines the most basic implementation of AbstractFunction
    All function implementations must inherit from this.
'''
from lambdacore.environment import Environment
from lambdacore.abstract_function import AbstractFunction

class Function(AbstractFunction):
    def __init__(self, env: Environment):
        self.env = env 

    def initialise(self):
        return True

    def invoke(self):
        return None
