from typing import Final

from simple_serial_protocol.common import Byte
from simple_serial_protocol.param_type.ParamType import ParamType


class ParamTypeChar(ParamType[str]):
    NAME: Final[str] = "char"

    def __init__(self) -> None:
        super().__init__()
        self.__raw_data: str = ""
        self.__full: bool = False

    def get_length(self) -> int:
        return 1

    def get_buffer(self, data: str) -> bytes:
        return data.encode('ascii')

    def reset(self) -> None:
        self.__raw_data = ""
        self.__full = False

    def add_byte(self, byte: Byte) -> None:
        if self.is_full():
            raise RuntimeError("Added byte to already filled  param var.")
        self.__full = True
        self.__raw_data = chr(byte)

    def is_full(self) -> bool:
        return self.__full

    def get_data(self) -> str:
        return self.__raw_data

    def dispose(self) -> None:
        self.__raw_data = None
