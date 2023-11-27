import logging
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "mylog.log")


def setup_logger(name: str):
    """Конфигуратор логгера"""
    logging.basicConfig(filename=PATH, filemode="w+", level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)
