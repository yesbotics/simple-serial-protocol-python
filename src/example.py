import sys
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from simple_serial_protocol import Baudrate, CommandParam, SimpleSerialProtocol
from simple_serial_protocol.common import Byte
from simple_serial_protocol.param_type.ParamTypeInt16 import ParamTypeInt16
from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8
from simple_serial_protocol.param_type.ParamTypeBoolean import ParamTypeBoolean
from simple_serial_protocol.param_type.ParamTypeByte import ParamTypeByte
from simple_serial_protocol.param_type.ParamTypeUnsignedInt16 import ParamTypeUnsignedInt16
from simple_serial_protocol.param_type.ParamTypeUnsignedInt8 import ParamTypeUnsignedInt8


class Example:
    def __init__(self, portname: str, baudrate: Baudrate):
        self.arduino: SimpleSerialProtocol = SimpleSerialProtocol(portname, baudrate)
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
    ):
        print('Received several values from Arduino:')
        print('byte_value', byte_value)
        print('boolean_value', boolean_value)
        print('int8Value', int8Value)
        print('uint8Value', uint8Value)
        print('int16Value', int16Value)
        print('uint16Value', uint16Value)
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
