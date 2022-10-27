# coding: utf-8

from abc import ABC, abstractmethod


class Comm(ABC):
    @abstractmethod
    def recv(self, buf: bytearray, offset: int, length: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def send(self, data: bytes) -> int:
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError
