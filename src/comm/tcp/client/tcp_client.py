# coding: utf-8

from socket import socket
from threading import Thread
from typing import Callable, Dict, List
from src.connection import (
    Connection,
    ConnectionState,
    Method,
    OnActionListener,
)
from src.definitions.prop_keys import PropKeys
from src.log.logger import Logger, DefaultLogger
from src.utils.props import PropsUtils


class TcpClient(Connection):
    PROPERTY_PORT_DEFAULT = 8884
    PROPERTY_MIN_RECONNECT_RETRY_TIME_DEFAULT = 4
    PROPERTY_MAX_RECONNECT_RETRY_TIME_DEFAULT = 32
    SECOND_TO_MILLISECOND = 1000

    def __init__(self):
        self.__is_init = False
        self.__connection_state = ConnectionState.DISCONNECTED
        self.__tcp_socket = None
        self.__logger = DefaultLogger()
        self.__on_connection_state_changed_listener_list: \
            List[Callable[[ConnectionState, Exception], None]] = []
        self.__address = ''
        self.__port = TcpClient.PROPERTY_PORT_DEFAULT
        self.__auto_reconnect = False
        self.__min_reconnect_retry_time = \
            TcpClient.PROPERTY_MIN_RECONNECT_RETRY_TIME_DEFAULT
        self.__max_reconnect_retry_time = \
            TcpClient.PROPERTY_MAX_RECONNECT_RETRY_TIME_DEFAULT
        self.__current_reconnect_retry_time = \
            self.__min_reconnect_retry_time

    def set_logger(self, logger: Logger):
        self.__logger = logger

    def add_on_connection_state_changed_listener(
            self,
            listener: Callable[[ConnectionState, Exception], None]):
        if listener not in self.__on_connection_state_changed_listener_list:
            self.__on_command_listener_list.append(listener)

    def remove_on_connection_state_changed_listener(
            self,
            listener: Callable[[ConnectionState, Exception], None]):
        self.__on_connection_state_changed_listener_list.remove(listener)

    def init(self, config_props: Dict[str, str]):
        self.__address = PropsUtils.get_prop_str(
            config_props,
            PropKeys.PROP_IP,
            ''
        )
        self.__port = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_PORT,
            TcpClient.PROPERTY_PORT_DEFAULT
        )
        self.__auto_reconnect = PropsUtils.get_prop_bool(
            config_props,
            PropKeys.PROP_AUTO_CONNECT,
            False
        )
        self.__min_reconnect_retry_time = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_AUTO_CONNECT,
            TcpClient.PROPERTY_MIN_RECONNECT_RETRY_TIME_DEFAULT
        )
        self.__max_reconnect_retry_time = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_MAX_RECONNECT_RETRY_TIME,
            TcpClient.PROPERTY_MAX_RECONNECT_RETRY_TIME_DEFAULT
        )
        self.__current_reconnect_retry_time = min(
            self.__max_reconnect_retry_time,
            self.__min_reconnect_retry_time
        )

        self.__tcp_connect(self)
        self.__is_init = True

    def __tcp_connect_task(self):
        # self.__subscribe_manager.clear()
        self.__tcp_socket = socket()

    def __tcp_connect(self):
        thread = Thread(target=self.__tcp_connect_task)
        thread.start()

    def close(self):
        raise NotImplementedError

    def getState(self) -> ConnectionState:
        return self.__connection_state

    def publish(
        self,
        topic: str,
        method: Method,
        data: bytes,
        on_action_listener: OnActionListener = None
    ):
        raise NotImplementedError

    def subscribe(
        self,
        topic: str,
        method: Method,
        on_data_listener: Callable[[str, Method, bytes], None],
        on_action_listener: OnActionListener = None
    ):
        raise NotImplementedError

    def unsubscribe(self, topic: str, method: Method):
        raise NotImplementedError
