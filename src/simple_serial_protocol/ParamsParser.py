from typing import Any, Final, Type

from simple_serial_protocol.param_type.ParamType import ParamType
from simple_serial_protocol.common import Byte
from simple_serial_protocol.exception import ParamTypeUnknownException, ParserTooManyBytesException


class ParamsParser:
    __TYPES: Final[dict[str, Type[ParamType]]] = {}

    @staticmethod
    def has_type(name: str) -> Any:
        return name in ParamsParser.__TYPES

    @staticmethod
    def get_type(name: str) -> Any:
        return ParamsParser.__TYPES.get(name)

    @staticmethod
    def add_type(name: str, clazz: Type[ParamType]) -> None:
        ParamsParser.__TYPES[name] = clazz

    def __init__(self, type_names: list[str] = None) -> None:
        self.__type_names: Final[list[str]] = type_names
        self.__types_length: Final[int] = len(type_names) if type_names is not None else None
        self._types: list[ParamType] | None = None
        self.__type_index: int | None = None
        self.__current_type: ParamType | None = None
        if len(self.__type_names) > 0:
            self._types = []
            for type_name in self.__type_names:
                if type_name in ParamsParser.__TYPES:
                    clazz: Type[ParamType] = ParamsParser.__TYPES.get(type_name)
                    inst: ParamType = clazz()
                    self._types.append(inst)
                else:
                    raise ParamTypeUnknownException
            self.__current_type = self._types[0]
            self.__type_index = 0

    def add_byte(self, byte: Byte) -> None:
        if self._types is None:
            raise RuntimeError("Tried to add byte to params but no types defined.")
        if self.__current_type.is_full():
            # print("parser - is full", byte)
            self.__type_index += 1
            if self.__type_index >= self.__types_length:
                raise ParserTooManyBytesException
            self.__current_type = self._types[self.__type_index]
        self.__current_type.add_byte(byte)

    def is_full(self) -> bool:
        if self._types is not None:
            if self.__type_index < (self.__types_length - 1):
                #  * Not reached last type
                # print("not reached last type")
                return False
            else:
                #  * Last type filled?
                # // print("last type filled")
                return self.__current_type.is_full()
        else:
            #  * No types defined -> always full
            # // print("no types defined")
            return True

    def reset(self) -> None:
        if self._types is not None:
            for t in self._types:
                t.reset()
        self.__type_index = 0
        self.__current_type = self._types[0]

    def get_data(self) -> list[Any]:
        return [t.get_data() for t in self._types]

    def dispose(self) -> None:
        for t in self._types:
            t.dispose()
