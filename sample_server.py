# coding: utf-8

from cconn.comm.bus.cross_connection_bus import CrossConnectionBus
from cconn.connection_factory import ConnectionType
from cconn.definitions.prop_keys import PropKeys


if __name__ == '__main__':
    bus = CrossConnectionBus()
    bus.start(
        connection_type=ConnectionType.TCP,
        server_config={
            PropKeys.PROP_PORT: 11001,
        },
        network_register_config={
            PropKeys.PROP_UDP_REGISTER_FLAG: 0xfffe1234,
            PropKeys.PROP_UDP_REGISTER_SERVER_PORT: 11001,
            PropKeys.PROP_UDP_REGISTER_BROADCAST_PORT: 12000,
            PropKeys.PROP_UDP_REGISTER_BROADCAST_INTERVAL: 3000,
        }
    )

    input()

    bus.stop_all()

