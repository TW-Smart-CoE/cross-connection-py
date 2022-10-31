# coding: utf-8

import time
from concurrent.futures import ThreadPoolExecutor
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from typing import Callable, Dict, List
from cconn.comm.base.msg import Msg, MsgHeader, MsgType
from cconn.comm.base.comm_handler import CommHandler
from cconn.comm.base.pubsub.client_comm_pubsub_manager import (
    ClientCommPubSubManager)
from cconn.comm.base.pubsub.subscription import Subscription
from cconn.comm.base.topic_mapper import TopicMapper
from cconn.comm.tcp.tcp_comm import TcpComm
from cconn.connection import (
    Connection,
    ConnectionState,
    Method,
    OnActionListener,
)
from cconn.definitions.prop_keys import PropKeys
from cconn.log.logger import Logger, DefaultLogger
from cconn.utils.message_converter import MessageConverter
from cconn.utils.props import PropsUtils


class TcpClient(Connection):
    PROPERTY_PORT_DEFAULT = 8884
    PROPERTY_MIN_RECONNECT_RETRY_TIME_DEFAULT = 4
    PROPERTY_MAX_RECONNECT_RETRY_TIME_DEFAULT = 32
    SECOND_TO_MILLISECOND = 1000

    def __init__(self):
        self.__is_init = False
        self.__connection_state = ConnectionState.DISCONNECTED
        self.__tcp_socket = None
        self.__comm_handler = None
        self.__logger = DefaultLogger()
        self.__subscribe_manager = ClientCommPubSubManager(self.__logger)
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
        self.__executor = ThreadPoolExecutor(max_workers=5)

    def set_logger(self, logger: Logger):
        self.__logger = logger
        self.__subscribe_manager.set_logger(logger)

    def add_on_connection_state_changed_listener(
            self,
            listener: Callable[[ConnectionState, Exception], None]):
        if listener not in self.__on_connection_state_changed_listener_list:
            self.__on_connection_state_changed_listener_list.append(listener)

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
            PropKeys.PROP_MIN_RECONNECT_RETRY_TIME,
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

        self.__tcp_connect()
        self.__is_init = True

    def __close_task(self):
        if self.__comm_handler is not None:
            self.__comm_handler.close()

        self.__subscribe_manager.clear()
        self.__address = ''
        self.__port = TcpClient.PROPERTY_PORT_DEFAULT
        self.__auto_reconnect = False
        self.__is_init = False

    def close(self):
        self.__executor.submit(self.__close_task)

    def __change_connection_state(
        self, state:
        ConnectionState,
        e: Exception = None
    ):
        self.__connection_state = state
        if state == ConnectionState.CONNECTED:
            self.__current_reconnect_retry_time = \
                self.__min_reconnect_retry_time

        for listener in self.__on_connection_state_changed_listener_list:
            listener(state, e)

    def __schedule_reconnect_task(self):
        self.__change_connection_state(ConnectionState.RECONNECTING)
        self.__logger.info(
            'schedule tcp reconnect attempt in {0} seconds.'.format(
                self.__current_reconnect_retry_time))

        time.sleep(self.__current_reconnect_retry_time)
        self.__current_reconnect_retry_time = \
            min(self.__current_reconnect_retry_time * 2,
                self.__max_reconnect_retry_time)

        self.__logger.info('tcp do reconnecting ...')
        self.__tcp_connect()

    def __on_comm_close(self, comm_handler: CommHandler, is_passive: bool):
        if is_passive and self.__auto_reconnect:
            self.__executor.submit(self.__schedule_reconnect_task)

    def __on_msg_arrived(self, comm_handler: CommHandler, msg: Msg):
        if msg.header.type != MsgType.PUBLISH:
            pass

        self.__subscribe_manager.invoke_matched_callback(
            MessageConverter.bytes_to_str(msg.topic),
            msg.data,
        )

    def __tcp_connect_task(self):
        self.__subscribe_manager.clear()
        self.__tcp_socket = socket(AF_INET, SOCK_STREAM)

        self.__comm_handler = CommHandler(
            is_client=True,
            comm=TcpComm(
                tcp_socket=self.__tcp_socket,
                address=self.__address,
                port=self.__port,
            ),
            logger=self.__logger,
            on_comm_close_listener=self.__on_comm_close,
            on_msg_arrived_listener=self.__on_msg_arrived,
            on_conn_state_changed_listener=self.__change_connection_state,
        )

        self.__executor.submit(self.__comm_handler.run)

    def __tcp_connect(self):
        thread = Thread(target=self.__tcp_connect_task)
        thread.start()

    def get_state(self) -> ConnectionState:
        return self.__connection_state

    def __publish_task(
            self,
            topic: str,
            method: Method,
            data: bytes,
            on_action_listener: OnActionListener):
        full_topic = TopicMapper.to_full_topic(topic, method)
        full_topic_bytes = MessageConverter.str_to_bytes(full_topic)
        try:
            if self.__comm_handler is not None:
                send_len = self.__comm_handler.send(
                    Msg(
                        header=MsgHeader(
                            type=MsgType.PUBLISH,
                            method=method,
                        ),
                        topic=full_topic_bytes,
                        data=data,
                    )
                )

                if on_action_listener is not None:
                    if send_len > 0:
                        on_action_listener.on_success()
                    else:
                        on_action_listener.on_failure('Error send data failed')
            else:
                if on_action_listener is not None:
                    on_action_listener.on_failure(
                        Exception(
                            'Error send data failed: comm_hander is None'))
        except Exception as e:
            self.__logger.error(
                'Error occurred when sending data: {0}'.format(str(e)))
            if on_action_listener is not None:
                on_action_listener.on_failure(e)

    def publish(
        self,
        topic: str,
        method: Method,
        data: bytes,
        on_action_listener: OnActionListener = None
    ):
        if not self.__is_init:
            if on_action_listener is not None:
                on_action_listener.on_failure(Exception('TcpClient not init'))

            return

        self.__executor.submit(
            self.__publish_task, topic, method, data, on_action_listener)

    def __subscribe_task(
        self,
        topic: str,
        method: Method,
        on_data_listener: Callable[[str, Method, bytes], None],
        on_action_listener: OnActionListener
    ):
        full_topic = TopicMapper.to_full_topic(topic, method)
        full_topic_bytes = MessageConverter.str_to_bytes(full_topic)

        try:
            if self.__comm_handler is not None:
                send_len = self.__comm_handler.send(
                    Msg(
                        header=MsgHeader(
                            type=MsgType.SUBSCRIBE,
                            method=method,
                        ),
                        topic=full_topic_bytes,
                    )
                )

                if send_len > 0:
                    self.__subscribe_manager.subscribe(Subscription(
                        topic=full_topic,
                        callback=on_data_listener
                    ))

                    if on_action_listener is not None:
                        on_action_listener.on_success()
                else:
                    if on_action_listener is not None:
                        on_action_listener.on_failure('Error send data failed')
            else:
                if on_action_listener is not None:
                    on_action_listener.on_failure(
                        Exception(
                            'Error send data failed: comm_hander is None'))
        except Exception as e:
            self.__logger.error(
                'Error occurred when sending data: {0}'.format(str(e)))
            on_action_listener.on_failure(e)

    def subscribe(
        self,
        topic: str,
        method: Method,
        on_data_listener: Callable[[str, Method, bytes], None],
        on_action_listener: OnActionListener = None
    ):
        if not self.__is_init:
            if on_action_listener is not None:
                on_action_listener.on_failure(Exception('TcpClient not init'))

            return

        self.__executor.submit(
            self.__subscribe_task,
            topic,
            method,
            on_data_listener,
            on_action_listener
        )

    def __unsubscribe_task(self, topic: str, method: Method):
        full_topic = TopicMapper.to_full_topic(topic, method)
        full_topic_bytes = MessageConverter.str_to_bytes(full_topic)

        try:
            if self.__comm_handler is not None:
                send_len = self.__comm_handler.send(
                    Msg(
                        header=MsgHeader(
                            type=MsgType.UNSUBSCRIBE,
                            method=method,
                        ),
                        topic=full_topic_bytes,
                    )
                )

                if send_len > 0:
                    self.__subscribe_manager.unsubscribe(full_topic)
                else:
                    self.__logger.warn('unsubscribe Error send data failed')
            else:
                self.__logger.warn(
                    'unsubscribe: Error send data failed, comm_hander is None')
        except Exception as e:
            self.__logger.error(
                'Error occurred when sending data: {0}'.format(str(e)))

    def unsubscribe(self, topic: str, method: Method):
        if not self.__is_init:
            return

        self.__executor.submit(self.__unsubscribe_task, topic, method)
