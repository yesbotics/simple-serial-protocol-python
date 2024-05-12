import struct
from typing import Final

from simple_serial_protocol.common import Byte
from simple_serial_protocol.param_type.ParamType import ParamType


class ParamTypeBoolean(ParamType[bool]):
    NAME: Final[str] = "boolean"

    def __init__(self) -> None:
        super().__init__()
        self.__raw_data: bytearray = bytearray(self.get_length())
        self.__index: int | None = None

    def get_length(self) -> int:
        return 1

    def get_buffer(self, data: bool) -> bytes:
        return struct.pack('<?', data)

    def reset(self) -> None:
        self.__index = 0

    def add_byte(self, byte: Byte) -> None:
        if self.is_full():
            return
        self.__raw_data.append(byte)
        self.__index += 1

    def is_full(self) -> bool:
        return self.__index >= self.get_length()

    def get_data(self) -> bool:
        return self.__raw_data[0] == 1

    def dispose(self) -> None:
        self.__raw_data = None
