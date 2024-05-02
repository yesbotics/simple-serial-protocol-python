import importlib
from typing import Final, Type

from simple_serial_protocol.Baudrate import Baudrate
from simple_serial_protocol.serial_port.AbstractSerialPort import AbstractSerialPort
from simple_serial_protocol.serial_port.PySerialSerialPort import PySerialSerialPort

from simple_serial_protocol.serial_port.PySide6SerialPort import PySide6SerialPort


class SimpleSerialProtocol:

    @staticmethod
    def __create_serialport(
            portname: str,
            baudrate: Baudrate,
            serial_port_class: Type[AbstractSerialPort] = None
    ) -> AbstractSerialPort:
        if serial_port_class is not None:
            return serial_port_class(portname, baudrate)
        try:
            import PySide6
            return PySide6SerialPort(portname, baudrate)
        except ImportError:
            pass
        try:
            import serial
            return PySerialSerialPort(portname, baudrate)
        except ImportError:
            pass
        raise RuntimeError('No serial port library like pyserial could be found')

    def __init__(self, portname: str, baudrate: Baudrate):
        self.__serial_port: Final[AbstractSerialPort] = SimpleSerialProtocol.__create_serialport(portname, baudrate)
        po = SimpleSerialProtocol.__create_serialport(portname, baudrate)
        pass
