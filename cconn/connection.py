# coding: utf-8

from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Dict
from cconn.module import Module
from cconn.comm.base.msg import Method


class ConnectionState(Enum):
    CONNECTING = 0
    CONNECTED = 1
    DISCONNECTED = 2
    RECONNECTING = 3


class OnActionListener(ABC):
    @abstractmethod
    def on_success(self):
        raise NotImplementedError

    def on_failure(self, error: Exception):
        raise NotImplementedError


class Connection(Module):
    @abstractmethod
    def add_on_connection_state_changed_listener(
            self,
            listener: Callable[[ConnectionState, Exception], None]):
        raise NotImplementedError

    @abstractmethod
    def remove_on_connection_state_changed_listener(
            self,
            listener: Callable[[ConnectionState, Exception], None]):
        raise NotImplementedError

    @abstractmethod
    def init(self, config_props: Dict[str, str]):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def get_state(self) -> ConnectionState:
        raise NotImplementedError

    @abstractmethod
    def publish(
        self,
        topic: str,
        method: Method,
        data: bytes,
        on_action_listener: OnActionListener = None
    ):
        raise NotImplementedError

    @abstractmethod
    def subscribe(
        self,
        topic: str,
        method: Method,
        on_data_listener: Callable[[str, Method, bytes], None],
        on_action_listener: OnActionListener = None
    ):
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, topic: str, method: Method):
        raise NotImplementedError
