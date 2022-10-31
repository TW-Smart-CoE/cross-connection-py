# coding: utf-8

from cconn.comm.bus.cross_network_bus import CrossNetworkBus
from cconn.connection_factory import ConnectionType
from cconn.definitions.prop_keys import PropKeys

bus = CrossNetworkBus()
bus.start(
    connection_type=ConnectionType.TCP,
    server_config={
        PropKeys.PROP_PORT: '11000'
    },
    network_register_config={
        PropKeys.PROP_UDP_REGISTER_SERVER_PORT: '11000',
        PropKeys.PROP_UDP_REGISTER_BROADCAST_PORT: '12000',
        PropKeys.PROP_UDP_REGISTER_BROADCAST_INTERVAL: '3000',
    }
)

input()

bus.stop_all()
