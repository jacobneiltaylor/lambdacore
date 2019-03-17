'''
    Defines the interface for *Function objects 
'''

from .environment import Environment

class GenericFunction():
    def __init__(self, env):
        self.env = env

    def initialise(self) -> bool:
        return True

    def invoke(self):
        pass
