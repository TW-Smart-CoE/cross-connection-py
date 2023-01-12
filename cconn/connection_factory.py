# coding: utf-8

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

    def create_bus() -> Bus:
        return CrossConnectionBus()
