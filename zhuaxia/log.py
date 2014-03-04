# -*- coding:utf-8 -*-
import logging, logging.handlers
import os
import config

LVL_DICT={
        'debug' : logging.DEBUG,
        'info'  : logging.INFO,
        'error' : logging.ERROR,
        'warn'  : logging.WARNING
        }

#style dict
STYLE={
    'bold'    : u'\x1b[1m',
    'clear'   : u'\x1b[0m',
    'uline'   : u'\x1b[4m', # Underline Texth
    'error'   : u'\x1b[31;5m', #blink, bold, red
    'red'     : u'\x1b[31;1m', # bold, red
    'warning' : u'\x1b[33m', #blink, bold, yellow
    'cyan'    : u'\x1b[36m', #bold, cyan
    'green'   : u'\x1b[32m', #bold, cyan
    'purple'  : u'\x1b[35m', #bold, cyan
}

def test_hl():
    for x in STYLE:
        print hl("["+x+"]: this is test", x)

def hl(text,style_key):
    """highlight the give text"""
    k = style_key.lower()
    if k not in STYLE.keys():
        return text
    return ('%('+k+')s'+ text + '%(clear)s') % STYLE

def err(msg):
    """this is for normal error output before the logger was setup"""
    print hl('Error: ','error') + msg

def warn(msg):
    """this is for normal warning output before the logger was setup"""
    print hl('Warning: ','warning') + msg

class LogFormatter(logging.Formatter):
    """define different format for different log levels"""

    err_fmt  = hl('ERROR: ','error') +"%(msg)s"
    dbg_fmt  = "DEBUG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = "%(msg)s"
    warning_fmt = hl('WARNING: ','warning') + "%(msg)s"

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)


    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = LogFormatter.dbg_fmt
        elif record.levelno == logging.INFO:
            self._fmt = LogFormatter.info_fmt
        elif record.levelno == logging.ERROR:
            self._fmt = LogFormatter.err_fmt
        elif record.levelno == logging.WARNING:
            self._fmt = LogFormatter.warning_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result

def setup_log(c_lvl_str, f_lvl_str):
    """setup_log, this function should be called only once at the beginning of application starts"""
    file_lvl = LVL_DICT[f_lvl_str.lower()]
    console_lvl = LVL_DICT[c_lvl_str.lower()]

    logger = logging.getLogger('zhuaxiaLogger')
    logger.setLevel(file_lvl)

    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler( \
            os.path.join(config.USER_PATH,'zhuaxia.log'), \
           maxBytes=5000000, backupCount=5 )
    fh.setLevel(file_lvl)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(console_lvl)

    # create formatter and add it to the handlers
    fhFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    chFormatter = LogFormatter()

    fh.setFormatter(fhFormatter)
    ch.setFormatter(chFormatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.debug("Log system setup successfully")

def get_logger():
    return logging.getLogger('zhuaxiaLogger')