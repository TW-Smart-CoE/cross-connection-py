# coding: utf-8

from collections import deque
from threading import Thread, Lock, Semaphore
from typing import Callable


class MsgThread(Thread):
    def __init__(self, on_msg_arrived: Callable[[any], None]):
        Thread.__init__(self)
        self.__lock = Semaphore(0)
        self.__mutex = Lock()
        self.is_running = False
        self.__queue = deque()
        self.__key = False
        self.__on_msg_arrived = on_msg_arrived

    def start(self):
        if self.is_running:
            return False

        super().start()

    def stop(self):
        if self.is_running:
            self.enqueue(None)
            self.join()

    def enqueue(self, msg: any):
        if self.is_running:
            with self.__mutex:
                self.__queue.append(msg)

            self.__set_key()

    def __msg_arrived(self, msg: any):
        self.__on_msg_arrived(msg)

    def __reset_key(self):
        self.__key = False

    def __wait_for_key(self):
        if not self.__key:
            self.__lock.acquire()

    def __reset_key(self):
        self.__key = False

    def __set_key(self):
        if not self.__key:
            self.__key = True
            self.__lock.release()

    def __pop_msg(self):
        with self.__mutex:
            return self.__queue.popleft()

    def __clear_queue(self):
        with self.__mutex:
            self.__queue.clear()

    def __is_empty(self):
        with self.__mutex:
            return len(self.__queue) == 0

    def __reset_key_if_empty(self):
        with self.__mutex:
            if len(self.__queue) == 0:
                self.__reset_key()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.__wait_for_key()

            if not self.__is_empty():
                msg = self.__pop_msg()

                if msg is not None:
                    self.__msg_arrived(msg)
                else:
                    self.__clear_queue()
                    break

            self.__reset_key_if_empty()

        self.is_running = False
