"""
    lambdacore.run Implementation
"""
from .environment import Environment

STR_ENTER_LOG = '_enter'
STR_EXIT_LOG = '_exit'

def run(event, context):
    """
        LambdaCore entrypoint
    """

    log_vars = {
        'func_name': context.function_name,
        'func_ver': context.function_version,
        'request': context.aws_request_id
    }

    retval = None

    env = Environment(event, context)

    env.logs.emit(STR_ENTER_LOG, log_vars)

    if env.load():
        retval = env.exec()

    env.logs.emit(STR_EXIT_LOG, log_vars)

    return retval
