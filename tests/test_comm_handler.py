# coding: utf-8

from unittest import TestCase
from src.comm.base.comm import Comm
from src.comm.base.comm_handler import CommHandler
from src.comm.base.msg import Msg, MsgType, Method
from src.log.logger import DefaultLogger
from src.utils.message_converter import MessageConvert


class MockComm(Comm):
    def recv(self, buf: bytearray, offset: int, len: int) -> int:
        msg = Msg()
        msg.header.type = MsgType.UNSUBSCRIBE.value
        msg.header.method = Method.QUERY.value
        msg.header.check_sum = 0
        msg.topic = MessageConvert.str_to_bytes('/aaaa')
        msg.data = MessageConvert.str_to_bytes('00000000')
        msg.prepare()

        buf[offset:] = msg.to_bytes()
        return msg.length()

    def send(self, data: bytes) -> int:
        return len(data)

    def connect(self):
        print('connect ok')

    def close(self):
        pass
     

class TestCommHandler(TestCase):
    def setUp(self):
        self.__buffer = bytearray(16)
        for i in range (0, 16):
            self.__buffer[i] = i
    
    def test_handler(self):
        comm_handler = CommHandler(
            is_client=True,
            comm=MockComm(),
            logger=DefaultLogger(),
            on_comm_close_listener=lambda handler, b: print(
                'close (passive = {0})'.format(b)),
            on_msg_arrived_listener=lambda msg: print(msg.length()),
            on_connection_state_changed_listener=lambda state, e: print(state.name, e)
        )

        comm_handler.start()

    # def test_buffer_copy(self):
    #     print(bytes_to_hex_format(self.__buffer))
    #     self.__buffer[0:8] = self.__buffer[4:12]
    #     print(bytes_to_hex_format(self.__buffer))

    # def test_struct_unkpack_from(self):
    #     print(struct.unpack_from('>B', self.__buffer, 5))

    # def test_buffer_copy(self):
    #     buffer = bytes(self.__buffer)

    #     dst_buffer = bytes(buffer)
    #     dst_buffer[2] = 3

    #     for i in range(0, 16):
    #         print(buffer[i])