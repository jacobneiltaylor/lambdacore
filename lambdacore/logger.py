"""
    lambadcore.Logger implementation
"""

import logging
import json

_DCT_SEVERITY = {
    'DEBUG': lambda log, msg: log.debug(msg),
    'INFO': lambda log, msg: log.info(msg),
    'WARN': lambda log, msg: log.warning(msg),
    'ERROR': lambda log, msg: log.error(msg),
    'CRIT': lambda log, msg: log.critical(msg),
}

_STR_UNDEF_LOG = 'Undefined log "{}"'
_STR_MISSING_VAR = 'Variable "{}" not defined in request to emit named log "{}"'

_STR_DATA_DIR = 'data'
_STR_LOG_MSG_FILE = 'logs.json'

_STR_LOG_LEVEL_ENVVAR = 'LMDCORE_LOG_LEVEL'

class Logger():
    """
        Represents the log registry, which enables users to separate  
    """

    def __init__(self, log_level: str, default_named_logs: dict):
        self._logger = logging.getLogger()
        self._logger.setLevel(log_level)
        self._log_registry = default_named_logs

    def register(self, named_logs:dict):
        """
            Register named log messages with the logger
        """
        # TODO: Sanity check keys in dict
        self._log_registry.update(named_logs)

    def emit(self, log_name:str, log_vars:dict=dict()):
        """
            Emits a defined log message that has been registered with the environment.
        """
        try:
            log = self._log_registry[log_name]
        except KeyError:
            raise KeyError(_STR_UNDEF_LOG.format(log_name))
        
        message = log['msg']

        if 'vars' in log:
            self._assert_vars(log_name, log['vars'], log_vars.keys())
            message = message.format(**log_vars)
            
        self.emit_string(message, log['sev'])

    def emit_string(self, msg, sev='INFO'):
        """
            Logs a message provided as a string to the environment logger at a specified severity.
            Defaults to severity INFO.
        """
        _DCT_SEVERITY[sev](self._logger, msg)

    @staticmethod
    def _assert_vars(name, expect, actual):
        for var in expect:
            if var not in actual:
                raise KeyError(_STR_MISSING_VAR.format(var, name))
