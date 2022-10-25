# coding: utf-8

from typing import Dict
from src.comm.base.pubsub.subscription import Subscription
from src.comm.base.topic_mapper import TopicMapper
from src.log.logger import Logger
from src.utils.topic_utils import TopicUtils


class ClientCommPubSubManager:
    def __init__(self, logger: Logger):
        self.__logger: Logger = logger
        self.__subscription_dict: Dict[str, Subscription] = dict()

    def subscribe(self, subscription: Subscription):
        self.__subscription_dict[subscription.topic] = subscription

    def unsubscribe(self, topic: str):
        del self.__subscription_dict[topic]

    def clear(self):
        self.__subscription_dict.clear()

    def invoke_matched_callback(self, full_topic: str, data: bytes):
        for topic, subscription in self.__subscription_dict.items():
            if TopicUtils.is_topic_match(topic, full_topic):
                if subscription.callback is not None:
                    try:
                        app_topic, method = \
                            TopicMapper.to_app_topic(full_topic)
                        subscription.callback(app_topic, method, data)
                    except BaseException as e:
                        self.__logger.error(e)
