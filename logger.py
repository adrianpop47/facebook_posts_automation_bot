import logging
import sys


class Logger:

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("debug.log", mode='w'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def info(self, msg):
        logging.info(msg)

    def error(self, msg):
        logging.error(msg)
