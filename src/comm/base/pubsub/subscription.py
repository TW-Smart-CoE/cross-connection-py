# coding: utf-8

from dataclasses import dataclass
from typing import Callable
from src.comm.base.msg import Method


@dataclass
class Subscription:
    topic: str = None
    callback: Callable[[str, Method, bytes], None] = None
