# coding: utf-8

from abc import abstractmethod
from enum import Enum
from src.comm.tcp.client.tcp_client import TcpClient
from src.connection import Connection
from src.network.detect.network_detector import NetworkDetector
from src.network.detect.udp.udp_detector import UdpDetector


class ConnectionType(Enum):
    TCP = 1


class NetworkDiscoveryType(Enum):
    UDP = 2


class ConnectionFactory:
    @abstractmethod
    def create_connection(connection_type: ConnectionType) -> Connection:
        if connection_type == ConnectionType.TCP:
            return TcpClient()
        else:
            return None

    @abstractmethod
    def create_detector(
            network_discovery_type: NetworkDiscoveryType) -> NetworkDetector:
        if network_discovery_type == NetworkDiscoveryType.UDP:
            return UdpDetector()
        else:
            return None
