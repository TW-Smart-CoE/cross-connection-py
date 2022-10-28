# coding: utf-8

from typing import Dict


class PropsUtils:
    @staticmethod
    def get_prop_str(
        config_props: Dict,
        key: str,
        default_value: str,
    ) -> str:
        data = config_props.get(key)
        return default_value if data is None else data

    @staticmethod
    def get_prop_int(
        config_props: Dict,
        key: str,
        default_value: int,
    ) -> int:
        data = config_props.get(key)
        if data is None:
            return default_value
        else:
            try:
                data = int(data)
                return data
            except BaseException as e:
                print(e)
                return default_value

    @staticmethod
    def get_prop_float(
        config_props: Dict,
        key: str,
        default_value: float,
    ) -> float:
        data = config_props.get(key)
        if data is None:
            return default_value
        else:
            try:
                data = float(data)
                return data
            except BaseException as e:
                print(e)
                return default_value

    @staticmethod
    def get_prop_bool(
        config_props: Dict,
        key: str,
        default_value: bool,
    ) -> bool:
        data = config_props.get(key)
        if data is None:
            return default_value
        else:
            try:
                data = bool(data)
                return data
            except BaseException as e:
                print(e)
                return default_value
