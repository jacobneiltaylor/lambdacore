"""
    lambdacore.Environment Implementation
"""

import os
import json
import pydoc
import logging
import inspect
import functools

from .generic_function import GenericFunction
from .logger import Logger

_STR_DATA_DIR = 'data'
_STR_LOG_MSG_FILE = 'logs.json'

_STR_LOG_LEVEL_ENVVAR = 'LMDCORE_LOG_LEVEL'
_STR_MODULE_ENVVAR = 'LMDCORE_MODULE'
_STR_FUNCTION_ENVVAR = 'LMDCORE_FUNCTION'

_STR_DEFAULT_MODULE = 'lambdacore'
_STR_DEFAULT_FUNCTION = 'ExampleFunction'

_STR_SANDBOX_LOGS = '_sbox_{}_{}'
_TPL_SANDBOX_STATES = ( 
    'init',
    'fail',
    'done'
)

def sandboxed(func):
    log_name = lambda state: _STR_SANDBOX_LOGS.format(state, func.__name__)
    logs = {state: log_name(state) for state in _TPL_SANDBOX_STATES}

    @functools.wraps(func)
    def wrapper(*args):
        env: Environment = args[0]

        retval = None
        env.logs.emit(logs['init'], env.class_info)

        try:
            func(*args)

        except Exception as e:
            log_args = env.get_log_args(e)
            log_args.update(env.class_info)
            env.logs.emit(logs['fail'], log_args)

        else:
            env.logs.emit(logs['done'], env.class_info)

        finally:
            return retval

    return wrapper

class Environment():
    """
        Helps abstract runtime environment specifics from Lambda implementation
    """
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.logs = Logger(self._get_log_level(), self._get_module_logs())
        self.class_info = {
            "module_name": self.get_module_name(),
            "class_name": self.get_function_name()
        }

        self._function = None
        self._ready = False


    def _get_module_logs(self):
        filename = self._get_data_filename(_STR_LOG_MSG_FILE)
        with open(filename) as infile:
            return json.load(infile)


    @sandboxed
    def load(self):
        module = pydoc.locate(self.class_info["module_name"])
        self.function: GenericFunction = getattr(module, self.class_info["class_name"])(self)
        return self.function.initialise()


    @sandboxed
    def exec(self):
        return self.function.invoke()


    @staticmethod
    def get_module_name():
        return Environment.get_var(_STR_MODULE_ENVVAR, _STR_DEFAULT_MODULE)


    @staticmethod
    def get_function_name():
        return Environment.get_var(_STR_FUNCTION_ENVVAR, _STR_DEFAULT_FUNCTION)


    @staticmethod
    def _get_data_filename(filename):
        Environment.get_filename(_STR_DATA_DIR, filename)


    @staticmethod
    def get_filename(*args):
        """
            Gets a filename relative to the directory of the caller
        """
        frame = inspect.stack()[1]
        path = [os.path.dirname(frame[0].f_code.co_filename),] + args
        return os.path.join(*path)


    @staticmethod
    def _get_log_level():
        return getattr(
            logging,
            Environment.get_var(_STR_LOG_LEVEL_ENVVAR),
            logging.INFO)


    @staticmethod
    def get_var(var_name, default=None):
        """
            Returns an envvar value if it exists.
            Returns a specified fallback value (default None) if it doesn't.
        """
        return os.getenv(var_name, default)


    @staticmethod
    def get_log_args(e: Exception):
        return {
            'exception_type': type(e).__name__,
            'exception_msg': str(e)
        }
