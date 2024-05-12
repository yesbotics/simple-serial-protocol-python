from typing import Final

from simple_serial_protocol.common import Byte
from simple_serial_protocol.param_type.ParamType import ParamType


class ParamTypeString(ParamType[str]):
    NAME: Final[str] = "string"
    __CHAR_NULL: Final[int] = 0x00  # 0x00 // End of String

    def __init__(self) -> None:
        super().__init__()
        self._raw_data: str = ""
        self._full: bool = False

    def get_length(self) -> int:
        return len(self._raw_data)

    def get_buffer(self, data: str) -> bytes:
        # expand length for end-of-string char
        return data.encode('ascii') + bytes([ParamTypeString.__CHAR_NULL])

    def reset(self) -> None:
        self._raw_data = ""
        self._full = False

    def add_byte(self, byte: Byte) -> None:
        if self.is_full():
            raise RuntimeError("Added byte to already filled  param var.")
        if byte == ParamTypeString.__CHAR_NULL:
            self._full = True
            return
        self._raw_data += chr(byte)

    def is_full(self) -> bool:
        return self._full

    def get_data(self) -> str:
        return self._raw_data

    def dispose(self) -> None:
        self._raw_data = None
