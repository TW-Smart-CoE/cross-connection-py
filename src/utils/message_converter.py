# coding: utf-8

from typing import Final


class MessageConverter:
    ENCODEING_UTF8: Final = 'utf-8'

    @staticmethod
    def str_to_bytes(data: str) -> bytes:
        return data.encode(MessageConverter.ENCODEING_UTF8)

    def bytes_to_str(data: bytes) -> str:
        return data.decode(MessageConverter.ENCODEING_UTF8)
