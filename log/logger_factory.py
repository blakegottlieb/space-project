import logging
import logging.config
import time
from main_constants import *
from simulator.simulator_constants import SIM_LOG

GROUND_SYSTEM_LOG = 'SystemTest'
MAIN_LOG_LEVEL = logging.INFO


def indent(sys_depth):
    return "  " * sys_depth


def banner(msg, divider='-'):

    line_start = "\n%s|" % (indent(StandardLogger.LOG_TIMESTAMP_WIDTH))
    bars = divider * (StandardLogger.LOG_WIDTH - StandardLogger.LOG_TIMESTAMP_WIDTH)

    banner_ = \
        "%s%s" % (line_start, bars) + \
        "%s %s" % (line_start, msg) + \
        "%s%s" % (line_start, bars)
    return banner_


class StandardLogger(logging.Logger):
    # Standard log format for all applications
    FILE_NAMES = {
        SIM_LOG: 'sim_log.log',
        GROUND_SYSTEM_LOG: 'test_log.log'
    }
    DEFAULT_FILE_NAME = 'default_log.log'

    LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_TIMESTAMP_WIDTH = 12
    LOG_WIDTH = 80

    def __init__(self, logger_name):
        # create logger
        logging.Logger.__init__(self, logger_name)
        logger_ = logging.getLogger(logger_name)

        # Set log level
        if DEV_MODE:
            logger_.setLevel(logging.DEBUG)
        else:
            logger_.setLevel(MAIN_LOG_LEVEL)
        # create formatter
        log_formatter = logging.Formatter(StandardLogger.LOGGER_FORMAT)
        log_formatter.converter = time.gmtime

        # create handlers of log file + console
        logfile_main = logging.FileHandler(StandardLogger.FILE_NAMES.get(logger_name,
                                           StandardLogger.DEFAULT_FILE_NAME))
        console = logging.StreamHandler()

        logfile_main.setFormatter(log_formatter)
        console.setFormatter(log_formatter)

        logger_.addHandler(logfile_main)
        logger_.addHandler(console)

        msg = '            %s Logger Started' % logger_.name
        logger_.debug("\n\n\n")
        logger_.debug(banner(msg, "\\"))
