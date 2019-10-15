
import importlib
import logging

def load_writer_for_ext(ext):
    try:
        return importlib.import_module(ext, __package__)
    except ImportError as e:
        logging.error(str(e))
        return None