# coding: utf-8

from abc import ABC, abstractmethod
from cconn.log.logger import Logger


class Module(ABC):
    @abstractmethod
    def set_logger(self, logger: Logger):
        raise NotImplementedError
