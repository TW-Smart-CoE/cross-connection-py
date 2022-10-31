# coding: utf-8

import struct
from enum import Enum
from typing import Callable
from cconn.comm.base.comm import Comm
from cconn.comm.base.msg import (MSG_FLAG,
                                 MSG_HEADER_LEN,
                                 Msg,
                                 MsgHeader,
                                 calc_checksum)
from cconn.connection import ConnectionState
from cconn.log.logger import Logger


class MsgCompleteness(Enum):
    NONE = 0
    FLAG = 1
    HEADER = 2


class CommHandler:
    BUFFER_SIZE = 4096
    INT_SIZE_BYTE = 4

    def __init__(
        self,
        is_client: bool,
        comm: Comm,
        logger: Logger,
        on_comm_close_listener: Callable[[any, bool], None] = None,
        on_msg_arrived_listener: Callable[[any, Msg], None] = None,
        on_conn_state_changed_listener:
            Callable[[ConnectionState, Exception], None] = None,
    ):
        self.__is_close: bool = False
        self.__msg_completeness: MsgCompleteness = MsgCompleteness.NONE
        self.__is_client: bool = is_client
        self.__comm: Comm = comm
        self.__logger: Logger = logger
        self.__current_header: MsgHeader = MsgHeader()
        self.__current_msg: Msg = Msg()
        self.__on_comm_close_listener = \
            on_comm_close_listener
        self.__on_msg_arrived_listener = \
            on_msg_arrived_listener
        self.__on_connection_state_changed_listener = \
            on_conn_state_changed_listener
        self.__buffer: bytearray = bytearray(CommHandler.BUFFER_SIZE)
        self.__buffer_data_start_offset = 0
        self.__buffer_data_len = 0

    def __on_connection_state_changed(
            self,
            state: ConnectionState,
            e: Exception = None):
        if self.__on_connection_state_changed_listener is not None:
            self.__on_connection_state_changed_listener(state, e)

    def __on_comm_close(self, is_passive: bool):
        if self.__on_comm_close_listener is not None:
            self.__on_comm_close_listener(self, is_passive)

    def __on_msg_arrived(self, msg: Msg):
        if self.__on_msg_arrived_listener is not None:
            self.__on_msg_arrived_listener(self, msg)

    def run(self):
        if self.__is_client:
            try:
                self.__on_connection_state_changed(ConnectionState.CONNECTING)
                self.__comm.connect()
            except Exception as e:
                self.__logger.error('connect failed: {0}'.format(str(e)))
                self.close(True)
                return

        self.__on_connection_state_changed(ConnectionState.CONNECTED)

        self.__is_close = False
        while not self.__is_close:
            msg = self.__read_msg_flag_from_buffer()
            if msg is None:
                self.__logger.warn('Connection is lost')
                self.close(True)
                self.__is_close = True
            else:
                if calc_checksum(msg) == msg.header.check_sum:
                    self.__on_msg_arrived(msg)

                # clear completeness state
                self.__msg_completeness = MsgCompleteness.NONE

    def send(self, msg: Msg) -> int:
        if not self.__is_close:
            msg.prepare()
            return self.__comm.send(msg.to_bytes())
        else:
            return 0

    def close(self, is_passive: bool):
        if not is_passive:
            self.__on_msg_arrived_listener = None
            self.__on_comm_close_listener = None

        print('close')
        self.__is_close = True

        try:
            self.__comm.close()
            self.__on_connection_state_changed(ConnectionState.DISCONNECTED)
        except Exception as e:
            self.__logger.error(
                'Could not close the connection: {0}'.format(str(e)))
            self.__on_connection_state_changed(ConnectionState.DISCONNECTED, e)
        finally:
            self.__on_comm_close(is_passive)

    def __buffer_left_size(self) -> int:
        return CommHandler.BUFFER_SIZE - \
            (self.__buffer_data_start_offset + self.__buffer_data_len)

    def __read_msg_flag_from_buffer(self) -> Msg:
        found = False
        for i in range(self.__buffer_data_start_offset,
                       self.__buffer_data_start_offset +
                       self.__buffer_data_len -
                       CommHandler.INT_SIZE_BYTE
                       ):
            flag = struct.unpack_from(
                '>I',
                self.__buffer,
                self.__buffer_data_start_offset + i)
            if flag[0] == MSG_FLAG:
                found = True
                if i != 0:
                    self.__buffer[0:self.__buffer_data_len] = \
                        self.__buffer[i:i + self.__buffer_data_len]
                    self.__buffer_data_start_offset = 0
                    self.__buffer_data_len -= i

                break

        if found:
            self.__msg_completeness = MsgCompleteness.FLAG
            return self.__read_msg_header_from_buffer()
        else:
            self.__msg_completeness = MsgCompleteness.NONE
            self.__buffer_data_start_offset = 0
            self.__buffer_data_len = 0
            return self.__read_data()

    def __read_msg_header_from_buffer(self) -> Msg:
        if self.__buffer_data_len < MSG_HEADER_LEN:
            return self.__read_data()

        head_buffer = bytearray(MSG_HEADER_LEN)

        head_buffer[0:MSG_HEADER_LEN] = self.__buffer[
            self.__buffer_data_start_offset:
            self.__buffer_data_start_offset + MSG_HEADER_LEN]
        self.__current_header.from_bytes(bytes(head_buffer))
        self.__msg_completeness = MsgCompleteness.HEADER

        return self.__read_msg_body_from_buffer()

    def __read_msg_body_from_buffer(self) -> Msg:
        if self.__buffer_data_len < \
            MSG_HEADER_LEN + self.__current_header.topic_len + \
                self.__current_header.data_len:
            return self.__read_data()

        topic_buffer = bytearray(self.__current_header.topic_len)
        topic_buffer[0:self.__current_header.topic_len] = \
            self.__buffer[self.__buffer_data_start_offset + MSG_HEADER_LEN:
                          self.__buffer_data_start_offset + MSG_HEADER_LEN +
                          self.__current_header.topic_len]

        data_buffer = bytearray(self.__current_header.data_len)
        data_buffer[0:self.__current_header.data_len] = \
            self.__buffer[self.__buffer_data_start_offset + MSG_HEADER_LEN +
                          self.__current_header.topic_len:
                          self.__buffer_data_start_offset + MSG_HEADER_LEN +
                          self.__current_header.topic_len +
                          self.__current_header.data_len]

        self.__current_msg.header = self.__current_header
        self.__current_msg.topic = topic_buffer
        self.__current_msg.data = data_buffer

        left_data_len = self.__buffer_data_len - self.__current_msg.length()

        self.__buffer[0:left_data_len] = self.__buffer[
            self.__buffer_data_start_offset +
            self.__current_msg.length():
            self.__buffer_data_start_offset +
            self.__current_msg.length() + left_data_len
        ]

        self.__buffer_data_start_offset = 0
        self.__buffer_data_len = left_data_len

        return self.__current_msg.copy()

    def __read_data(self) -> Msg:
        length = 0
        try:
            length = self.__comm.recv(
                self.__buffer,
                self.__buffer_data_start_offset + self.__buffer_data_len,
                self.__buffer_left_size()
            )
        except Exception as e:
            self.__logger.warn('recv exception: {0}'.format(str(e)))
            return None

        if length <= 0:
            self.__logger.warn('recv len == {0}'.format(length))
            return None

        self.__buffer_data_len += length

        if self.__msg_completeness == MsgCompleteness.NONE:
            return self.__read_msg_flag_from_buffer()
        elif self.__msg_completeness == MsgCompleteness.FLAG:
            return self.__read_msg_header_from_buffer()
        elif self.__msg_completeness == MsgCompleteness.HEADER:
            return self.__read_msg_body_from_buffer()
        else:
            return None
