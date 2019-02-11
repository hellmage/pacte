# Copyright (c) 2017 App Annie Inc. All rights reserved.
import logging
import imp
import inspect
import os.path
from unittest import TestCase

logger = logging.getLogger('pacte.state')


def _collect_state_files(state_dir):
    if not os.path.exists(state_dir):
        logger.debug('Ignore file: %s', state_dir)
        return
    if os.path.isfile(state_dir):
        if state_dir.startswith('state_') and state_dir.endswith('.py'):
            yield os.path.split(state_dir)
        else:
            logger.debug('Ignore file: %s', state_dir)
    else:
        for dirpath, dirnames, filenames in os.walk(state_dir):
            for filename in filenames:
                if filename.startswith('state_') and filename.endswith('.py'):
                    yield dirpath, filename
                else:
                    logger.debug('Ignore file: %s', os.path.join(dirpath, filename))


def _import_state_module(dirpath, filename):
    if not dirpath.endswith('/'):
        dirpath += '/'
    module_name = filename[:-3]  # remove ".py" extension
    mod_f, mod_pathname, mod_desc = imp.find_module(module_name, [dirpath])
    full_module_name = dirpath.replace('/', '.') + module_name
    py = imp.load_module(full_module_name, mod_f, mod_pathname, mod_desc)
    for attr_name in dir(py):
        attr = getattr(py, attr_name)
        if inspect.isclass(attr):
            if attr_name.startswith('State') and issubclass(attr, TestCase) and getattr(attr, 'state', None):
                yield attr
            else:
                logger.debug('Ignore class: %s.%s', full_module_name, attr_name)


def load_states(state_dir):
    states = {}
    for dirpath, filename in _collect_state_files(state_dir):
        for cls in _import_state_module(dirpath, filename):
            states[cls.state] = cls
    return states
