import struct
from typing import Final

from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8


class ParamTypeInt64(ParamTypeInt8):
    NAME: Final[str] = "int64"

    def get_length(self) -> int:
        return 8

    def get_buffer(self, data: int) -> bytes:
        return struct.pack('<q', data)

    def get_data(self) -> int:
        return struct.unpack('<q', self._raw_data)[0]
