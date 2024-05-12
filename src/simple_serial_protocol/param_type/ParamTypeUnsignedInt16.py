import struct
from typing import Final

from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8


class ParamTypeUnsignedInt16(ParamTypeInt8):
    NAME: Final[str] = "unsigned_int16"

    def get_length(self) -> int:
        return 2

    def get_buffer(self, data: int) -> bytes:
        return struct.pack('<H', data)

    def get_data(self) -> int:
        return struct.unpack('<H', self._raw_data)[0]
