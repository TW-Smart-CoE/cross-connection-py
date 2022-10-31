# coding: utf-8

from typing import List
from cconn.comm.base.comm_server_wrapper import CommServerWrapper
from cconn.comm.base.msg import Msg, MsgType
from cconn.log.logger import Logger
from cconn.utils.message_converter import MessageConverter
from cconn.server import Server


class ServerCommPubSubManager:
    def __init__(self, logger: Logger):
        self.__logger: Logger = logger
        self.__comm_server_wrapper_list: List[CommServerWrapper] = []
        self.__server_callback: Server.Callback = None

    def set_logger(self, logger: Logger):
        self.__logger = logger

    def set_server_callback(self, callback: Server.Callback):
        self.__server_callback = callback

    def on_server_data_arrive(
            self,
            comm_server_wrapper: CommServerWrapper,
            msg: Msg
    ):
        if msg.header.type == MsgType.PUBLISH:
            self.__handle_publish(msg)
        elif msg.header.type == MsgType.SUBSCRIBE:
            self.__handle_subscribe(comm_server_wrapper, msg)
        elif msg.header.type == MsgType.UNSUBSCRIBE:
            self.__handle_unsubscribe(comm_server_wrapper, msg)

    def add_comm_wrapper(self, comm_server_wrapper: CommServerWrapper):
        self.__comm_server_wrapper_list.append(comm_server_wrapper)

    def remove_comm_wrapper(self, comm_server_wrapper: CommServerWrapper):
        self.__comm_server_wrapper_list.remove(comm_server_wrapper)

    def client_count(self):
        return len(self.__comm_server_wrapper_list)

    def clear_all_comm_wrappers(self):
        for it in self.__comm_server_wrapper_list:
            it.clear()
            it.comm_handler.close(False)

        self.__comm_server_wrapper_list.clear()

    def __handle_publish_msg_self(self, msg: Msg):
        full_topic = MessageConverter.bytes_to_str(msg.topic)

        for it in self.__comm_server_wrapper_list:
            if it.is_subscribed(full_topic):
                it.comm_handler.send(msg)

    def __handle_publish(self, msg: Msg):
        self.__handle_publish_msg_self(msg)

        # publish msg to bus
        if self.__server_callback is not None:
            self.__server_callback.on_publish(msg)

    def __handle_subscribe(
        self,
        comm_server_wrapper: CommServerWrapper,
        msg: Msg
    ):
        full_topic = MessageConverter.bytes_to_str(msg.topic)

        # subscribe topic self
        comm_server_wrapper.subscribe(full_topic)

        # subscribe topic to bus
        if self.__server_callback is not None:
            self.__server_callback.on_subscribe(full_topic)

    def __handle_unsubscribe(
        self,
        comm_server_wrapper: CommServerWrapper,
        msg: Msg
    ):
        full_topic = MessageConverter.bytes_to_str(msg.topic)

        # unsubscribe topic self
        comm_server_wrapper.unsubscribe(full_topic)

        # unsubscribe topic from bus
        if self.__server_callback is not None:
            self.__server_callback.on_unsubscribe(full_topic)
