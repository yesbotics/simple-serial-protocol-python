import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from simple_serial_protocol import Baudrate, ParamTypeString, SimpleSerialProtocol


class Example:
    def __init__(self, portname: str, baudrate: Baudrate):
        self.arduino: SimpleSerialProtocol = SimpleSerialProtocol(portname, baudrate)
        #  # or pass instance of an AbstractSerialPort implementation like PySerialSerialPort or PySide6SerialPort
        # self.arduino: SimpleSerialProtocol = SimpleSerialProtocol(PySerialSerialPort(str(portname), baudrate))
        self.is_running: bool = True

    def run(self) -> None:
        self.arduino.init()
        self.arduino.request___xxx(
            'i',
            [],
            self.on_response_id,
            [ParamTypeString.NAME],
        )
        while self.is_running:
            time.sleep(1)
        self.arduino.dispose()
        self.is_running = False

    def on_response_id(self, id_: str) -> None:
        print('on_response_id', id_)


def main() -> None:
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
