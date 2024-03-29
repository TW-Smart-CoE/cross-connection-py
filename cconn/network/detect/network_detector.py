# coding: utf-8

from abc import abstractmethod
from typing import Callable, Dict
from cconn.module import Module


class NetworkDetector(Module):
    @abstractmethod
    def start_discover(
        self,
        config_props: Dict[str, object],
        on_found_service: Callable[[Dict[str, object]], None]
    ):
        raise NotImplementedError

    @abstractmethod
    def stop_discover(self):
        raise NotImplementedError
