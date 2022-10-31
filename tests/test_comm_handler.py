# coding: utf-8

from concurrent.futures import ThreadPoolExecutor
from unittest import TestCase
from cconn.comm.base.comm import Comm
from cconn.comm.base.comm_handler import CommHandler
from cconn.comm.base.msg import Msg, MsgType, Method
from cconn.log.logger import DefaultLogger
from cconn.utils.message_converter import MessageConverter
     

class TestCommHandler(TestCase):
    def setUp(self):
        self.__thread_pool = ThreadPoolExecutor(max_workers=5)
    
    def test_handler_receive_one_packet(self):
        result = []
        class MockComm(Comm):
            def __init__(self):
                self.__read_count = 0
                self.msg = Msg()
                
            def recv(self, buf: bytearray, offset: int, len: int) -> int:
                if self.__read_count == 0:
                    self.__read_count += 1

                    self.msg.header.type = MsgType.UNSUBSCRIBE
                    self.msg.header.method = Method.QUERY
                    self.msg.header.check_sum = 0
                    self.msg.topic = MessageConverter.str_to_bytes('/aaaa')
                    self.msg.data = MessageConverter.str_to_bytes('00000000')
                    self.msg.prepare()

                    buf[offset:] = self.msg.to_bytes()
                    return self.msg.length()
                else:
                    return -1

            def send(self, data: bytes) -> int:
                return len(data)

            def connect(self):
                pass

            def close(self):
                pass


        comm = MockComm()
        comm_handler = CommHandler(
            is_client=True,
            comm=comm,
            logger=DefaultLogger(),
            on_comm_close_listener=lambda handler, b: print(
                'close (passive = {0})'.format(b)),
            on_msg_arrived_listener=lambda handler, msg: result.append(msg.length()),
            on_conn_state_changed_listener=lambda state, e: print(state.name, e)
        )

        future = self.__thread_pool.submit(comm_handler.run)
        future.result()

        self.assertEqual(comm.msg.length(), result[0])


    def test_handler_receive_half_packet(self):
        result = []
        class MockComm(Comm):
            def __init__(self):
                self.__read_count = 0
                self.msg = Msg()
                self.msg.header.type = MsgType.UNSUBSCRIBE
                self.msg.header.method = Method.QUERY
                self.msg.header.check_sum = 0
                self.msg.topic = MessageConverter.str_to_bytes('/aaaa')
                self.msg.data = MessageConverter.str_to_bytes('00000000')
                self.msg.prepare()
                
            def recv(self, buf: bytearray, offset: int, length: int) -> int:
                if self.__read_count == 0:
                    self.__read_count += 1
                    data = self.msg.to_bytes()[:10]
                    buf[offset:] = data
                    return len(data)
                elif self.__read_count == 1:
                    self.__read_count += 1
                    data = self.msg.to_bytes()[10:]
                    buf[offset:] = data
                    return len(data)
                else:
                    return 0

            def send(self, data: bytes) -> int:
                return len(data)

            def connect(self):
                pass

            def close(self):
                pass


        comm = MockComm()
        comm_handler = CommHandler(
            is_client=True,
            comm=comm,
            logger=DefaultLogger(),
            on_comm_close_listener=lambda handler, b: print(
                'close (passive = {0})'.format(b)),
            on_msg_arrived_listener=lambda handler, msg: result.append(msg.length()),
            on_conn_state_changed_listener=lambda state, e: print(state.name, e)
        )

        future = self.__thread_pool.submit(comm_handler.run)
        future.result()

        self.assertEqual(comm.msg.length(), result[0])

    def test_handler_receive_big_packet(self):
        result = []
        class MockComm(Comm):
            def __init__(self):
                self.__read_count = 0
                self.msg = Msg()
                self.msg.header.type = MsgType.UNSUBSCRIBE
                self.msg.header.method = Method.QUERY
                self.msg.header.check_sum = 0
                self.msg.topic = bytearray(128)
                self.msg.data = bytearray(4096) 
                self.msg.prepare()
                
            def recv(self, buf: bytearray, offset: int, length: int) -> int:
                if self.__read_count == 0:
                    self.__read_count += 1
                    data = self.msg.to_bytes()[:length]
                    buf[offset:] = data
                    return len(data)
                elif self.__read_count == 1:
                    self.__read_count += 1
                    data = self.msg.to_bytes()[CommHandler.BUFFER_SIZE:]
                    buf[offset:] = data
                    return len(data)
                else:
                    return 0

            def send(self, data: bytes) -> int:
                return len(data)

            def connect(self):
                pass

            def close(self):
                pass


        comm = MockComm()
        comm_handler = CommHandler(
            is_client=True,
            comm=comm,
            logger=DefaultLogger(),
            on_comm_close_listener=lambda handler, b: print(
                'close (passive = {0})'.format(b)),
            on_msg_arrived_listener=lambda handler, msg: result.append(msg.length()),
            on_conn_state_changed_listener=lambda state, e: print(state.name, e)
        )

        future = self.__thread_pool.submit(comm_handler.run)
        future.result()

        self.assertEqual(comm.msg.length(), result[0])

    def test_handler_receive_packet_concat(self):
        result = []
        class MockComm(Comm):
            def __init__(self):
                self.__read_count = 0
                self.msg1 = Msg()
                self.msg1.header.type = MsgType.UNSUBSCRIBE
                self.msg1.header.method = Method.QUERY
                self.msg1.header.check_sum = 0
                self.msg1.topic = bytearray(128)
                self.msg1.data = bytearray(256) 
                self.msg1.prepare()

                self.msg2 = Msg()
                self.msg2.header.type = MsgType.PUBLISH
                self.msg2.header.method = Method.REQUEST
                self.msg2.header.check_sum = 0
                self.msg2.topic = bytearray(188)
                self.msg2.data = bytearray(512) 
                self.msg2.prepare()
                
            def recv(self, buf: bytearray, offset: int, length: int) -> int:
                if self.__read_count == 0:
                    self.__read_count += 1
                    data1 = self.msg1.to_bytes()
                    data2 = self.msg2.to_bytes()
                    buf[offset:] = data1
                    buf[offset + len(data1):] = data2
                    return len(data1) + len(data2)
                else:
                    return 0

            def send(self, data: bytes) -> int:
                return len(data)

            def connect(self):
                pass

            def close(self):
                pass


        comm = MockComm()
        comm_handler = CommHandler(
            is_client=True,
            comm=comm,
            logger=DefaultLogger(),
            on_comm_close_listener=lambda handler, b: print(
                'close (passive = {0})'.format(b)),
            on_msg_arrived_listener=lambda handler, msg: result.append(msg.length()),
            on_conn_state_changed_listener=lambda state, e: print(state.name, e)
        )

        future = self.__thread_pool.submit(comm_handler.run)
        future.result()

        self.assertEqual(comm.msg1.length(), result[0])
        self.assertEqual(comm.msg2.length(), result[1])


    def test_handler_receive_packet_concat_recv_twice(self):
        result = []
        class MockComm(Comm):
            def __init__(self):
                self.__read_count = 0
                self.msg1 = Msg()
                self.msg1.header.type = MsgType.UNSUBSCRIBE
                self.msg1.header.method = Method.QUERY
                self.msg1.header.check_sum = 0
                self.msg1.topic = bytearray(128)
                self.msg1.data = bytearray(256) 
                self.msg1.prepare()

                self.msg2 = Msg()
                self.msg2.header.type = MsgType.PUBLISH
                self.msg2.header.method = Method.REQUEST
                self.msg2.header.check_sum = 0
                self.msg2.topic = bytearray(188)
                self.msg2.data = bytearray(512) 
                self.msg2.prepare()
                
            def recv(self, buf: bytearray, offset: int, length: int) -> int:
                if self.__read_count == 0:
                    self.__read_count += 1
                    data1 = self.msg1.to_bytes()
                    data2 = self.msg2.to_bytes()[:200]
                    buf[offset:] = data1
                    buf[offset + len(data1):] = data2
                    return len(data1) + len(data2)
                elif self.__read_count == 1:
                    self.__read_count += 2
                    data = self.msg2.to_bytes()[200:]
                    buf[offset:] = data
                    return len(data)
                else:
                    return 0

            def send(self, data: bytes) -> int:
                return len(data)

            def connect(self):
                pass

            def close(self):
                pass


        comm = MockComm()
        comm_handler = CommHandler(
            is_client=True,
            comm=comm,
            logger=DefaultLogger(),
            on_comm_close_listener=lambda handler, b: print(
                'close (passive = {0})'.format(b)),
            on_msg_arrived_listener=lambda handler, msg: result.append(msg.length()),
            on_conn_state_changed_listener=lambda state, e: print(state.name, e)
        )

        future = self.__thread_pool.submit(comm_handler.run)
        future.result()

        self.assertEqual(comm.msg1.length(), result[0])
        self.assertEqual(comm.msg2.length(), result[1])
