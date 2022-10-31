# coding: utf-8

from abc import abstractmethod
from typing import Dict
from cconn.module import Module


class NetworkRegister(Module):
    @abstractmethod
    def register(
        self,
        config_props: Dict[str, str]
    ):
        raise NotImplementedError

    @abstractmethod
    def unregister(self):
        raise NotImplementedError
