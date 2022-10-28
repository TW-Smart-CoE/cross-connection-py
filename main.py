# coding: utf-8

from typing import Dict
from src.connection import ConnectionState
from src.connection_factory import ConnectionFactory, ConnectionType, NetworkDiscoveryType
from src.definitions.prop_keys import PropKeys
from src.utils.message_converter import MessageConverter
from src.utils.props import PropsUtils
from src.comm.base.msg import Method

TEST_TOPIC = 'command/cluster'

detector = ConnectionFactory.create_detector(NetworkDiscoveryType.UDP)
connection = ConnectionFactory.create_connection(ConnectionType.TCP)

def on_data_arrived(topic: str, method: Method, data: bytes):
   print(topic)
   print(method)
   print(MessageConverter.bytes_to_str(data))

def on_conn_state_changed(conn_state: ConnectionState, e: Exception):
   print(conn_state)
   if conn_state == ConnectionState.CONNECTED:
      connection.subscribe('command/+', Method.REQUEST, on_data_arrived)

connection.add_on_connection_state_changed_listener(on_conn_state_changed)

def on_found_service(config_props: Dict[str, str]):
   detector.stop_discover()

   ip = PropsUtils.get_prop_str(config_props, PropKeys.PROP_UDP_DETECTOR_ON_FOUND_SERVICE_IP, '')
   port = PropsUtils.get_prop_int(config_props, PropKeys.PROP_UDP_DETECTOR_BROADCAST_PORT, 0)

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
