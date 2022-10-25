# coding: utf-8

from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def verbose(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def debug(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def info(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def warn(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def wtf(self, message: str):
        raise NotImplementedError


def DefaultLogger(Logger):
    def verbose(self, message: str):
        print('[VERBOSE] {0}'.format(message))

    def debug(self, message: str):
        print('[DEBUG] {0}'.format(message))

    def info(self, message: str):
        print('[INFO] {0}'.format(message))

    def warn(self, message: str):
        print('[WARN] {0}'.format(message))

    def error(self, message: str):
        print('[ERROR] {0}'.format(message))

    def wtf(self, message: str):
        print('[WTF] {0}'.format(message))
