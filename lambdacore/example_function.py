from .generic_function import GenericFunction

class ExampleFunction(GenericFunction):
    def invoke(self):
        self.env.logs('Running from ExampleFunction')
