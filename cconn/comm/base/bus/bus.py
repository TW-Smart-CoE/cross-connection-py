# coding: utf-8

from abc import abstractmethod
from cconn.comm.base.msg import Msg
from cconn.connection_factory import ConnectionType
from cconn.server import Server
from typing import Dict


class Bus:
    @abstractmethod
    def initialize(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def start(
            self,
            connectionType: ConnectionType,
            server_config: Dict[str, str],
            network_register_config: Dict[str, str]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def stop_all(self):
        raise NotImplementedError

    @abstractmethod
    def publish_msg_to_bus(msg: Msg, exclude_server: Server):
        raise NotImplementedError
