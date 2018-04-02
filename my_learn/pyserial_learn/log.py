# -*- encoding:utf-8 -*-
import logging


class Log(object):

    def __init__(self):
        pass

    def write_to_log(self, flag, my_str):
        logger_name = "example"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        # create file handler
        log_path = "./log.log"
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)

        # create formatter
        # fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
        fmt = "%(asctime)s %(message)s"
        datefmt = "%a %d %b %Y %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        # add handler and formatter to logger
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info(flag + ":" + my_str)

log = Log()

if __name__ == "__main__":

    log.write_to_log('1', 'han')

