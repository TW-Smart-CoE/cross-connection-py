# connection-py

cross-connection is used to provide a cross-protocol pub/sub-mode connection library among multiple devices in LAN.

### Features

- Pub/Sub connection similar to mqtt protocol.
- Network register/detection for auto connection when device reboot.
- Auto connection when network disconnect/reconnected.
- Cross protocol (TCP/IP, Bluetooth(support on [android library](https://github.com/TW-Smart-CoE/cross-connection-android))) connection. 

### Platform support

[android](https://github.com/TW-Smart-CoE/cross-connection-android)

[python](https://github.com/TW-Smart-CoE/cross-connection-py)


### Environment

python 3.9+

### Install

```
pip install -U cross-connection
```

### Sample

Server

```
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
            PropKeys.PROP_UDP_REGISTER_SERVER_PORT: 11001,
            PropKeys.PROP_UDP_REGISTER_BROADCAST_PORT: 12000,
            PropKeys.PROP_UDP_REGISTER_BROADCAST_INTERVAL: 3000,
        }
    )

    input()

    bus.stop_all()
```

Client
```
# coding: utf-8

from typing import Dict
from cconn.connection import ConnectionState
from cconn.connection_factory import ConnectionFactory, ConnectionType, NetworkDiscoveryType
from cconn.definitions.prop_keys import PropKeys
from cconn.utils.message_converter import MessageConverter
from cconn.utils.props import PropsUtils
from cconn.comm.base.msg import Method


TEST_TOPIC = '/execute_cmd_list'

detector = ConnectionFactory.create_detector(NetworkDiscoveryType.UDP)
connection = ConnectionFactory.create_connection(ConnectionType.TCP)

def on_data_arrived(topic: str, method: Method, data: bytes):
   print(topic)
   print(method)
   print(MessageConverter.bytes_to_str(data))

def on_conn_state_changed(conn_state: ConnectionState, e: Exception):
   print(conn_state)
   if conn_state == ConnectionState.CONNECTED:
      connection.subscribe(TEST_TOPIC, Method.REQUEST, on_data_arrived)

connection.add_on_connection_state_changed_listener(on_conn_state_changed)

def on_found_service(config_props: Dict[str, str]):
   detector.stop_discover()

   ip = PropsUtils.get_prop_str(config_props, PropKeys.PROP_UDP_DETECTOR_ON_FOUND_SERVICE_IP, '')
   port = PropsUtils.get_prop_int(config_props, PropKeys.PROP_UDP_DETECTOR_ON_FOUND_SERVICE_PORT, 0)

   print(f'found {ip} {port}')

   if ip != '' and port != 0:
      props = dict()
      props[PropKeys.PROP_IP] = ip
      props[PropKeys.PROP_PORT] = port
      props[PropKeys.PROP_AUTO_CONNECT] = str(True)
      props[PropKeys.PROP_MAX_RECONNECT_RETRY_TIME] = str(8)

      connection.init(props)


if __name__ == '__main__':
   detector.start_discover(
      config_props=dict(),
      on_found_service=on_found_service
   )

   count = 1
   while True:
      input()
      if connection.get_state() == ConnectionState.CONNECTED:
         connection.publish(TEST_TOPIC, Method.REQUEST, MessageConverter.str_to_bytes('data {0}'.format(count)))

      count += 1

```
