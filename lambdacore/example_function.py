from lambdacore.function import Function

_STR_EXAMPLE_MESSAGE = "Hello, world!"

class ExampleFunction(Function):
    def invoke(self):
        self.env.logs.emit_string(_STR_EXAMPLE_MESSAGE)
