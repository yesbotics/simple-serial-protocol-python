import struct
from typing import Final

from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8


class ParamTypeFloat(ParamTypeInt8):
    NAME: Final[str] = "float"

    def get_length(self) -> float:
        return 4

    def get_buffer(self, data: int) -> bytes:
        return struct.pack('<f', data)

    def get_data(self) -> int:
        return struct.unpack('<f', self._raw_data)[0]
