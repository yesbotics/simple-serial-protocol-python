import struct
from typing import Final

from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8


class ParamTypeUnsignedInt64(ParamTypeInt8):
    NAME: Final[str] = "unsigned_int64"

    def get_length(self) -> int:
        return 8

    def get_buffer(self, data: int) -> bytes:
        return struct.pack('<Q', data)

    def get_data(self) -> int:
        return struct.unpack('<Q', self._raw_data)[0]
