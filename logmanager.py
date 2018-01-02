#!/usr/bin/env python
import logging
from logging.config import fileConfig


class LogManager(object):
    def __init__(self):
        self.log_level = "INFO"
        fileConfig('logging_config.ini')
        #logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

    @staticmethod
    def logger():
        return logging.getLogger()
