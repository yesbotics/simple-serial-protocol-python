import struct
from typing import Final

from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8


class ParamTypeUnsignedInt32(ParamTypeInt8):
    NAME: Final[str] = "unsigned_int32"

    def get_length(self) -> int:
        return 4

    def get_buffer(self, data: int) -> bytes:
        return struct.pack('<I', data)

    def get_data(self) -> int:
        return struct.unpack('<I', self._raw_data)[0]
