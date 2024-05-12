from typing import Final

from serial import Serial

from simple_serial_protocol.Baudrate import Baudrate
from simple_serial_protocol.serial_port.AbstractSerialPort import AbstractSerialPort
from simple_serial_protocol.common import Byte


class PySerialSerialPort(AbstractSerialPort):

    def __init__(self, portname: str, baudrate: Baudrate):
        super().__init__(portname, baudrate)
        self.__serial_port: Final[Serial] = Serial()

    @property
    def is_open(self) -> bool:
        return self.__serial_port.is_open

    def open(self) -> None:
        self.__serial_port.port = self._portname
        self.__serial_port.baudrate = self._baudrate
        self.__serial_port.open()
        if not self.is_open:
            raise RuntimeError(f"Serialport '{self._portname}' not open")

    def close(self) -> None:
        self.__serial_port.close()

    def available(self) -> int:
        return self.__serial_port.in_waiting

    def read(self) -> Byte:
        bites: bytes = self.__serial_port.read()
        return bites[0]

    def write(self, buffer: bytes) -> None:
        self.__serial_port.write(buffer)
