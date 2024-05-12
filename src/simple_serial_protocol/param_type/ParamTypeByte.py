from typing import Final

from simple_serial_protocol.param_type.ParamTypeUnsignedInt8 import ParamTypeUnsignedInt8


class ParamTypeByte(ParamTypeUnsignedInt8):
    NAME: Final[str] = "byte"
