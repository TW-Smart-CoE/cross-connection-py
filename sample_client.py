# coding: utf-8

from typing import Dict, Final
from cconn.connection import ConnectionState
from cconn.connection_factory import ConnectionFactory
from cconn.definitions.prop_keys import PropKeys
from cconn.definitions.types import ConnectionType, NetworkDiscoveryType
from cconn.utils.data_converter import DataConverter
from cconn.utils.props import PropsUtils
from cconn.comm.base.msg import Method


TEST_TOPIC: Final = '/execute_cmd_list'
DETECT_FLAG: Final = 0xfffe1234


detector = ConnectionFactory.create_detector(NetworkDiscoveryType.UDP)
connection = ConnectionFactory.create_connection(ConnectionType.TCP)


def on_data_arrived(topic: str, method: Method, data: bytes):
   print(topic)
   print(method)
   print(DataConverter.bytes_to_str(data))


def on_conn_state_changed(conn_state: ConnectionState, e: Exception):
   print(conn_state)
   if conn_state == ConnectionState.CONNECTED:
      connection.subscribe(TEST_TOPIC, Method.REQUEST, on_data_arrived)
      connection.subscribe('/chat/response', Method.REPORT, on_data_arrived)
      connection.subscribe('/auto_play', Method.REQUEST, on_data_arrived)


connection.add_on_connection_state_changed_listener(on_conn_state_changed)


def on_found_service(config_props: Dict[str, object]):
   detector.stop_discover()
   print(config_props)

   ip = PropsUtils.get_prop_str(config_props, PropKeys.PROP_SERVER_IP, '')
   port = PropsUtils.get_prop_int(config_props, PropKeys.PROP_SERVER_PORT, 0)
   data = PropsUtils.get_prop_bytes(config_props, PropKeys.PROP_BROADCAST_DATA, None)

   print(f'found {ip} {port}')
   if ip != '' and port != 0:
      connection.start({
         PropKeys.PROP_IP: ip,
         PropKeys.PROP_PORT: port,
         PropKeys.PROP_AUTO_RECONNECT: True,
         PropKeys.PROP_MAX_RECONNECT_RETRY_TIME: 8,
         PropKeys.PROP_RECV_BUFFER_SIZE: 8192,
      })
   
   if data is not None:
      print(DataConverter.bytes_to_str(data))


def cleanup():
   print('stop discover')
   detector.stop_discover()

   print('disconnect')
   connection.close()


if __name__ == '__main__':
   detector.start_discover(
      config_props={
         PropKeys.PROP_FLAG: DETECT_FLAG,
         PropKeys.PROP_BROADCAST_PORT: 12000,
         PropKeys.PROP_BROADCAST_DEBUG_MODE: True,
      },
      on_found_service=on_found_service
   )

   count = 1
   while True:
      try:
         input()
      except KeyboardInterrupt:
         cleanup()         
         break

      if connection.get_state() == ConnectionState.CONNECTED:
          connection.publish(TEST_TOPIC, Method.REQUEST,
                             DataConverter.str_to_bytes('data {0}'.format(count)))

      count += 1

