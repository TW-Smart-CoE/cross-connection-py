# coding: utf-8

from dataclasses import dataclass
from typing import Dict
from cconn.server import Server
from cconn.comm.base.bus.bus import Bus
from cconn.comm.base.bus.server_struct import ServerStruct
from cconn.comm.base.msg import Msg
from cconn.connection_factory import (
    ConnectionFactory,
    ConnectionType,
    NetworkDiscoveryType
)
from cconn.comm.tcp.server.tcp_server import TcpServer
from cconn.utils.msg_thread import MsgThread


@dataclass
class MsgObjPublish:
    msg: Msg = None
    exclude_server: Server = None


class CrossNetworkBus(Bus):
    class ServerCallback(Server.Callback):
        def __init__(self, server: Server, bus: Bus):
            self.__server: Server = server
            self.__bus: Bus = bus

        def on_subscribe(self, full_topic: str):
            pass

        def on_unsubscribe(self, full_topic: str):
            pass

        def on_publish(self, msg: Msg):
            self.__bus.publish_msg_to_bus(msg, self.__server)

    def __init__(self):
        self.__initialized = False
        self.__server_dict: Dict[ConnectionType, ServerStruct] = dict()
        self.__msg_thread = None
        self.__initialize()

    def __msg_handler(self, msg_obj: any):
        if isinstance(msg_obj, MsgObjPublish):
            for server_struct in self.__server_dict.values():
                if server_struct.server != msg_obj.exclude_server:
                    server_struct.server.handle_publish_message(msg_obj.msg)

    def __initialize(self) -> bool:
        if self.__initialized:
            return True

        self.__create_message_processing_thread()

        tcp_server = TcpServer()
        tcp_server.set_callback(self.__create_server_callback(tcp_server))
        self.__server_dict[ConnectionType.TCP] = \
            ServerStruct(
                server=tcp_server,
                register=ConnectionFactory.create_register(
                    NetworkDiscoveryType.UDP)
        )

        self.__initialized = True
        return self.__initialized

    def start(
            self,
            connection_type: ConnectionType,
            server_config: Dict[str, str],
            network_register_config: Dict[str, str]) -> bool:
        if connection_type not in self.__server_dict:
            return False

        server_struct = self.__server_dict[connection_type]
        is_started = server_struct.server.start(server_config)
        if not is_started:
            return False

        server_struct.register.register(network_register_config)
        return is_started

    def stop_all(self):
        self.__msg_thread.stop()

        for it in self.__server_dict.values():
            it.register.unregister()
            it.server.stop()

    def __create_server_callback(self, server: Server) -> ServerCallback:
        return CrossNetworkBus.ServerCallback(server, self)

    def publish_msg_to_bus(self, msg: Msg, exclude_server: Server):
        self.__msg_thread.enqueue(MsgObjPublish(
            msg=msg,
            exclude_server=exclude_server,
        ))

    def __create_message_processing_thread(self):
        self.__msg_thread = MsgThread(self.__msg_handler)
        self.__msg_thread.start()
