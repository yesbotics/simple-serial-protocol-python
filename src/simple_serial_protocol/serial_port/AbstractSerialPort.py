from abc import ABC, abstractmethod
from typing import Final

from simple_serial_protocol.Baudrate import Baudrate
from simple_serial_protocol.common import Byte


class AbstractSerialPort(ABC):

    def __init__(self, portname: str, baudrate: Baudrate):
        self._portname: Final[str] = portname
        self._baudrate: Final[Baudrate] = baudrate

    @property
    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def available(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def read(self) -> Byte:
        raise NotImplementedError

    @abstractmethod
    def write(self, buffer: bytes) -> None:
        raise NotImplementedError
