# coding: utf-8


from abc import abstractmethod
from typing import Dict
from cconn.module import Module
from cconn.comm.base.msg import Msg


class Server(Module):
    class Callback:
        @abstractmethod
        def on_subscribe(self, full_topic: str):
            raise NotImplementedError

        @abstractmethod
        def on_unsubscribe(self, full_topic: str):
            raise NotImplementedError

        @abstractmethod
        def on_publish(self, msg: Msg):
            raise NotImplementedError

    @abstractmethod
    def start(self, config_props: Dict[str, str]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def handle_publish_message(self, msg: Msg):
        raise NotImplementedError

    @abstractmethod
    def set_callback(self, callback: Callback):
        raise NotImplementedError
