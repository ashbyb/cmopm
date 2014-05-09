__title__ = 'cmopm'
__version__ = '0.0.1'
__author__ = 'Brendan Ashby'
__email__ = 'brendanevansashby@gmail.com'
__license__ = 'CC BY-NC-SA 4.0'
__copyright__ = 'Copyright 2014 Brendan Ashby'

import logging
from logging import FileHandler, StreamHandler

default_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(module)s.%(funcName)s@L%(lineno)d:%(message)s")

console_handler = StreamHandler()
console_handler.setFormatter(default_formatter)

debug_handler = FileHandler("cmopm_debug.log", "a")
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(default_formatter)

error_handler = FileHandler("cmopm_error.log", "a")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(default_formatter)

root = logging.getLogger("cmopm")
root.addHandler(console_handler)
root.addHandler(debug_handler)
root.addHandler(error_handler)
root.setLevel(logging.DEBUG)