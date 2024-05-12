import struct
from typing import Final
from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8


class ParamTypeUnsignedInt8(ParamTypeInt8):
    NAME: Final[str] = "unsigned_int8"

    def get_length(self) -> int:
        return 1

    def get_buffer(self, data: int) -> bytes:
        return struct.pack('B', data)

    def get_data(self) -> int:
        return struct.unpack('B', self._raw_data)[0]
