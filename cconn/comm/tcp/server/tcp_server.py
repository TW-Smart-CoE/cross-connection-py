# coding: utf-8

from concurrent.futures import ThreadPoolExecutor
from functools import partial, partialmethod
from http import client
from socket import AF_INET, SOCK_STREAM, socket
from typing import Dict
from cconn.comm.base.comm_handler import CommHandler
from cconn.comm.base.comm_server_wrapper import CommServerWrapper
from cconn.comm.base.msg import Msg
from cconn.comm.base.pubsub.server_comm_pubsub_manager import \
    ServerCommPubSubManager
from cconn.comm.tcp.tcp_comm import TcpComm
from cconn.definitions.prop_keys import PropKeys
from cconn.log.logger import DefaultLogger, Logger
from cconn.server import Server
from cconn.utils.props import PropsUtils


class TcpServer(Server):
    PROPERTY_PORT_DEFAULT = 8884

    def __init__(self):
        self.__server_sock: socket = None
        self.__port: int = TcpServer.PROPERTY_PORT_DEFAULT
        self.__logger: Logger = DefaultLogger()
        self.__server_pub_sub_manager = ServerCommPubSubManager(self.__logger)
        self.__executor = ThreadPoolExecutor(max_workers=5)

    def set_logger(self, logger: Logger):
        self.__logger = logger
        self.__server_pub_sub_manager.set_logger(logger)

    def start(self, config_props: Dict[str, str]) -> bool:
        self.__port = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_PORT,
            TcpServer.PROPERTY_PORT_DEFAULT
        )

        if self.__server_sock is not None and self.__server_sock._:
            self.stop()

        self.__server_sock = socket(AF_INET, SOCK_STREAM)
        print(f'bind {self.__port}')
        self.__server_sock.bind(('', self.__port))
        self.__server_sock.listen()

        self.__executor.submit(self.__start_server_task)

        return True

    def __on_comm_close(
        self,
        comm_handler: CommHandler,
        is_passive: bool,
    ):
        self.__server_pub_sub_manager.remove_comm_wrapper(comm_handler.wrapper)
        client_count = self.__server_pub_sub_manager.client_count()
        self.__logger.debug(
            f'current client count = {client_count}')

    def __on_msg_arrived(
        self,
        comm_handler: CommHandler,
        msg: Msg
    ):
        self.__server_pub_sub_manager.on_server_data_arrive(
            comm_handler.wrapper, msg)

    def __start_server_task(self):
        while self.__server_sock is not None:
            client_sock = None
            address = ''
            try:
                client_sock, address = self.__server_sock.accept()
            except Exception as e:
                self.__logger.error(
                    f"tcp server socket's accept() failed: {str(e)}")
                self.__clear_clients()

            if client_sock is not None:
                comm_handler = CommHandler(
                        is_client=False,
                        comm=TcpComm(
                            tcp_socket=client_sock,
                            address=address[0],
                            port=address[1],
                        ),
                        logger=self.__logger,
                        on_comm_close_listener=self.__on_comm_close,
                        on_msg_arrived_listener=self.__on_msg_arrived,
                    )
                server_wrapper = CommServerWrapper(
                   comm_handler=comm_handler
                )
                comm_handler.wrapper = server_wrapper

                self.__server_pub_sub_manager.add_comm_wrapper(server_wrapper)
                client_count = self.__server_pub_sub_manager.client_count()
                self.__logger.debug(
                    f'current client count = {client_count}')
                self.__executor.submit(server_wrapper.comm_handler.run)

    def __clear_clients(self):
        self.__server_pub_sub_manager.clear_all_comm_wrappers()
        client_count = self.__server_pub_sub_manager.client_count()
        self.__logger.debug(
            f'current client count = {client_count}')

    def stop(self):
        try:
            if self.__server_sock is not None:
                self.__server_sock.close()
        except Exception as e:
            self.__logger.error(f'tcp server socket close failed: {e.message}')
        finally:
            self.__server_sock = None

        self.__clear_clients()
        self.__port = TcpServer.PROPERTY_PORT_DEFAULT

    def handle_publish_message(self, msg: Msg):
        self.__server_pub_sub_manager.__handle_publish_msg_self(msg)

    def set_callback(self, callback: Server.Callback):
        self.__server_pub_sub_manager.set_server_callback(callback)
