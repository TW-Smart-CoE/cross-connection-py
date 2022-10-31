# coding: utf-8

from enum import Enum
from cconn.comm.tcp.client.tcp_client import TcpClient
from cconn.connection import Connection
from cconn.network.detect.network_detector import NetworkDetector
from cconn.network.detect.udp.udp_detector import UdpDetector
from cconn.network.register.network_register import NetworkRegister
from cconn.network.register.udp.udp_register import UdpRegister


class ConnectionType(Enum):
    TCP = 1


class NetworkDiscoveryType(Enum):
    UDP = 2


class ConnectionFactory:
    def create_connection(connection_type: ConnectionType) -> Connection:
        if connection_type == ConnectionType.TCP:
            return TcpClient()
        else:
            return None

    def create_detector(
            network_discovery_type: NetworkDiscoveryType) -> NetworkDetector:
        if network_discovery_type == NetworkDiscoveryType.UDP:
            return UdpDetector()
        else:
            return None

    def create_register(
            network_discovery_type: NetworkDiscoveryType) -> NetworkRegister:
        if network_discovery_type == NetworkDiscoveryType.UDP:
            return UdpRegister()
        else:
            return None
