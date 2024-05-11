import sys
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path

from simple_serial_protocol import SimpleSerialProtocol
from simple_serial_protocol.Baudrate import Baudrate


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

    print('starte')
    arduino: SimpleSerialProtocol = SimpleSerialProtocol(args_parsed.portname, args_parsed.baudrate)
    arduino.registerCommand()
    arduino.init()
    time.sleep(3)
    arduino.dispose()
    print('stoppe')


if __name__ == '__main__':
    main()
