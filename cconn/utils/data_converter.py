# coding: utf-8

from typing import Final


class DataConverter:
    ENCODEING_UTF8: Final = 'utf-8'

    @staticmethod
    def str_to_bytes(data: str) -> bytes:
        return data.encode(DataConverter.ENCODEING_UTF8)

    @staticmethod
    def bytes_to_str(data: bytes) -> str:
        return data.decode(DataConverter.ENCODEING_UTF8)
