import sys
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from simple_serial_protocol import Baudrate, CommandParam, PySerialSerialPort, SimpleSerialProtocol
from simple_serial_protocol.common import Byte
from simple_serial_protocol.param_type.ParamTypeChar import ParamTypeChar
from simple_serial_protocol.param_type.ParamTypeFloat import ParamTypeFloat
from simple_serial_protocol.param_type.ParamTypeInt16 import ParamTypeInt16
from simple_serial_protocol.param_type.ParamTypeInt32 import ParamTypeInt32
from simple_serial_protocol.param_type.ParamTypeInt64 import ParamTypeInt64
from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8
from simple_serial_protocol.param_type.ParamTypeBoolean import ParamTypeBoolean
from simple_serial_protocol.param_type.ParamTypeByte import ParamTypeByte
from simple_serial_protocol.param_type.ParamTypeString import ParamTypeString
from simple_serial_protocol.param_type.ParamTypeUnsignedInt16 import ParamTypeUnsignedInt16
from simple_serial_protocol.param_type.ParamTypeUnsignedInt32 import ParamTypeUnsignedInt32
from simple_serial_protocol.param_type.ParamTypeUnsignedInt64 import ParamTypeUnsignedInt64
from simple_serial_protocol.param_type.ParamTypeUnsignedInt8 import ParamTypeUnsignedInt8


class Example:
    def __init__(self, portname: str, baudrate: Baudrate):
        self.arduino: SimpleSerialProtocol = SimpleSerialProtocol(portname,baudrate)
        #  # or pass instance of an AbstractSerialPort implementation like PySerialSerialPort or PySide6SerialPort
        # self.arduino: SimpleSerialProtocol = SimpleSerialProtocol(PySerialSerialPort(str(portname), baudrate))
        self.is_running: bool = True

    def run(self):
        self.arduino.registerCommand(
            's',
            self.on_got_command,
            [
                ParamTypeByte.NAME,
                ParamTypeBoolean.NAME,
                ParamTypeInt8.NAME,
                ParamTypeUnsignedInt8.NAME,
                ParamTypeInt16.NAME,
                ParamTypeUnsignedInt16.NAME,
                ParamTypeInt32.NAME,
                ParamTypeUnsignedInt32.NAME,
                ParamTypeInt64.NAME,
                ParamTypeUnsignedInt64.NAME,
                ParamTypeFloat.NAME,
                ParamTypeChar.NAME,
                ParamTypeString.NAME,
                ParamTypeString.NAME,
                ParamTypeString.NAME,
            ]
        )
        self.arduino.init()
        self.arduino.write_command(
            'r',
            [
                CommandParam(type=ParamTypeByte.NAME, value=0xff),
                CommandParam(type=ParamTypeBoolean.NAME, value=True),
                CommandParam(type=ParamTypeInt8.NAME, value=-128),
                CommandParam(type=ParamTypeUnsignedInt8.NAME, value=255),
                CommandParam(type=ParamTypeInt16.NAME, value=-32768),
                CommandParam(type=ParamTypeUnsignedInt16.NAME, value=65523),
                CommandParam(type=ParamTypeInt32.NAME, value=-2147483648),
                CommandParam(type=ParamTypeUnsignedInt32.NAME, value=4294967295),
                CommandParam(type=ParamTypeInt64.NAME, value=-2147483648000999),
                CommandParam(type=ParamTypeUnsignedInt64.NAME, value=7294967295000999),
                CommandParam(type=ParamTypeFloat.NAME, value=-1.23456789101112),
                CommandParam(type=ParamTypeChar.NAME, value='J'),
                CommandParam(type=ParamTypeString.NAME, value="text1: Hey, I'm text one!"),
                CommandParam(type=ParamTypeString.NAME, value="text2: And I am his brother text two!"),
                CommandParam(type=ParamTypeString.NAME, value="text3: Nice!"),
            ]
        )
        while self.is_running:
            time.sleep(1)
        self.arduino.dispose()

    def on_got_command(
            self,
            byte_value: Byte,
            boolean_value: bool,
            int8Value: int,
            uint8Value: int,
            int16Value: int,
            uint16Value: int,
            int32Value: int,
            uint32Value: int,
            int64Value: int,
            uint64Value: int,
            floatValue: float,
            charValue: str,
            stringValue1: str,
            stringValue2: str,
            stringValue3: str,
    ):
        print('Received several values from Arduino:')
        print('byte_value', byte_value)
        print('boolean_value', boolean_value)
        print('int8Value', int8Value)
        print('uint8Value', uint8Value)
        print('int16Value', int16Value)
        print('uint16Value', uint16Value)
        print('int32Value', int32Value)
        print('uint32Value', uint32Value)
        print('int64Value', int64Value)
        print('uint64Value', uint64Value)
        print('floatValue', floatValue)
        print('charValue', charValue)
        print('stringValue1', stringValue1)
        print('stringValue2', stringValue2)
        print('stringValue3', stringValue3)

        self.is_running = False


def main():
    arg_parser: ArgumentParser = ArgumentParser()
    arg_parser.add_argument(
        '--portname',
        '-p',
        help='serial port name',
        required=False,
        type=Path,
        default='/dev/ttyUSB0',
    )
    arg_parser.add_argument(
        '--baudrate',
        '-b',
        help='baud rate',
        required=False,
        type=int,
        default=Baudrate.BAUD_9600,
    )
    args_parsed: Namespace = arg_parser.parse_args()

    Example(args_parsed.portname, args_parsed.baudrate).run()


if __name__ == '__main__':
    main()
