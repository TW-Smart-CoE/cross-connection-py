# coding: utf-8

from typing import Optional
from cconn.bus.bus import Bus
from cconn.bus.cross_connection_bus import CrossConnectionBus
from cconn.comm.tcp.client.tcp_client import TcpClient
from cconn.connection import Connection
from cconn.definitions.types import ConnectionType, NetworkDiscoveryType
from cconn.network.detect.network_detector import NetworkDetector
from cconn.network.detect.udp.udp_detector import UdpDetector
from cconn.network.register.network_register import NetworkRegister
from cconn.network.register.udp.udp_register import UdpRegister


class ConnectionFactory:
    @staticmethod
    def create_connection(connection_type: ConnectionType) -> Connection:
        if connection_type == ConnectionType.TCP:
            return TcpClient()
        else:
            raise RuntimeError('Unsupported connection type')

    @staticmethod
    def create_detector(
            network_discovery_type: NetworkDiscoveryType) -> NetworkDetector:
        if network_discovery_type == NetworkDiscoveryType.UDP:
            return UdpDetector()
        else:
            raise RuntimeError('Unsupported detector type')

    @staticmethod
    def create_register(
            network_discovery_type: NetworkDiscoveryType) -> NetworkRegister:
        if network_discovery_type == NetworkDiscoveryType.UDP:
            return UdpRegister()
        else:
            raise RuntimeError('Unsupported register type')

    @staticmethod
    def create_bus() -> Bus:
        return CrossConnectionBus()
