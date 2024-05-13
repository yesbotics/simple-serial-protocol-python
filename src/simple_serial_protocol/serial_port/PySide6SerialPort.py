from typing import Final

from PySide6.QtCore import QIODevice
from PySide6.QtSerialPort import QSerialPort

from simple_serial_protocol import Baudrate
from simple_serial_protocol.common import Byte
from simple_serial_protocol.serial_port.AbstractSerialPort import AbstractSerialPort


class PySide6SerialPort(AbstractSerialPort):

    def __init__(self, portname: str, baudrate: Baudrate):
        super().__init__(portname, baudrate)
        self.__serial_port: Final[QSerialPort] = QSerialPort()

    @property
    def is_open(self) -> bool:
        return self.__serial_port.isOpen()

    def open(self) -> None:
        self.__serial_port.setPortName(self._portname)
        self.__serial_port.setBaudRate(self._baudrate)
        self.__serial_port.open(QIODevice.OpenModeFlag.ReadWrite)
        if not self.is_open:
            raise RuntimeError(f"Serialport '{self._portname}' not open")

    def close(self) -> None:
        self.__serial_port.close()

    def available(self) -> int:
        return self.__serial_port.bytesAvailable()

    def read(self) -> Byte:
        bites: bytes = self.__serial_port.read(1)
        return bites.data()[0]

    def write(self, buffer: bytes) -> None:
        self.__serial_port.write(buffer)