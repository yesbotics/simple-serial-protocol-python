from abc import ABC, abstractmethod
from typing import Final

from simple_serial_protocol.Baudrate import Baudrate


class AbstractSerialPort(ABC):

    def __init__(self, portname: str, baudrate: Baudrate):
        self.__portname: Final[str] = portname
        self.__baudrate: Final[Baudrate] = baudrate

    @abstractmethod
    def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
