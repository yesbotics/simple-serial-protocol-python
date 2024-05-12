from abc import ABC, abstractmethod
from typing import Generic, TypeAlias, TypeVar

from simple_serial_protocol.common import Byte

T: TypeAlias = TypeVar('T')


class ParamType(Generic[T], ABC):

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_byte(self, byte: Byte) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_full(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_data(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def dispose(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_buffer(self, data: T) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def get_length(self) -> int:
        raise NotImplementedError
