# coding: utf-8

from abc import abstractmethod
from cconn.comm.base.msg import Msg
from cconn.definitions.types import ConnectionType
from cconn.module import Module
from cconn.server import Server
from typing import Dict


class Bus(Module):
    @abstractmethod
    def initialize(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def start(
            self,
            connectionType: ConnectionType,
            server_config: Dict[str, object],
            network_register_config: Dict[str, object]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def stop_all(self):
        raise NotImplementedError

    @abstractmethod
    def publish_msg_to_bus(msg: Msg, exclude_server: Server):
        raise NotImplementedError
