from unittest import TestCase

from cconn.utils.msg_thread import MsgThread


class TestMsgThread(TestCase):
    def __msg_handler(self, msg: any):
        print(msg)

    def test_msg_thread(self):
        msg_thread = MsgThread(on_msg_arrived=self.__msg_handler)
        msg_thread.start()

        msg_thread.enqueue(1)
        msg_thread.enqueue(2)
        msg_thread.enqueue(3)
        msg_thread.enqueue(4)

        msg_thread.stop()
        