import struct
from typing import Final

from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8


class ParamTypeInt16(ParamTypeInt8):
    NAME: Final[str] = "int16"

    def get_length(self) -> int:
        return 2

    def get_buffer(self, data: int) -> bytes:
        return struct.pack('<h', data)

    def get_data(self) -> int:
        return struct.unpack('<h', self._raw_data)[0]
