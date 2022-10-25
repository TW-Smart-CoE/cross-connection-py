# coding: utf-8

import threading

from src.comm.base.comm import Comm
from src.log.logger import Logger


class CommHandler(threading.Thread):
    BUFFER_SIZE = 4096
    MSG_COMPLETENESS_NONE = 0
    MSG_COMPLETENESS_FLAG = 1
    MSG_COMPLETENESS_HEADER = 2

    def __init__(
        self,
        is_client: bool,
        comm: Comm,
        logger: Logger,
    ):
        threading.Thread.__init__(self)
        self.__is_close = False
        self.__msg_completeness = CommHandler.MSG_COMPLETENESS_NONE

    def run(self):
        pass
