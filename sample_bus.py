# coding: utf-8

import sys
from cconn.connection_factory import ConnectionFactory
from cconn.definitions.types import ConnectionType
from cconn.definitions.prop_keys import PropKeys


if __name__ == '__main__':
    bus = ConnectionFactory.create_bus()
    if not bus.initialize():
        print('Initialize failed')
        sys.exit(-1)

    bus.start(
        ConnectionType.TCP, {
            PropKeys.PROP_PORT: 11001,
            PropKeys.PROP_RECV_BUFFER_SIZE: 8192,
        }, {
            PropKeys.PROP_FLAG: 0xfffe1234,
            PropKeys.PROP_SERVER_PORT: 11001,
            PropKeys.PROP_BROADCAST_PORT: 12000,
            PropKeys.PROP_BROADCAST_INTERVAL: 3000,

        }
    )

    try:
        input()
    except KeyboardInterrupt:
        pass
    
    bus.stop_all()
