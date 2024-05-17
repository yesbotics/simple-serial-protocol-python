from dataclasses import dataclass
from threading import Event, Thread
from time import sleep
from typing import Any, Final, overload

from simple_serial_protocol.Baudrate import Baudrate
from simple_serial_protocol.ParamsParser import ParamsParser
from simple_serial_protocol.RegisteredCommand import RegisteredCommand
from simple_serial_protocol.common import Byte, CommandCallback, ErrorCallback
from simple_serial_protocol.exception import CommandAlreadyRegisteredException, CommandIsNotRegisteredException, \
    EotWasNotReadException, \
    ParamTypeIsAlreadyRegisteredException, \
    ParamTypeUnknownException
from simple_serial_protocol.param_type.ParamType import ParamType
from simple_serial_protocol.param_type.ParamTypeBoolean import ParamTypeBoolean
from simple_serial_protocol.param_type.ParamTypeByte import ParamTypeByte
from simple_serial_protocol.param_type.ParamTypeChar import ParamTypeChar
from simple_serial_protocol.param_type.ParamTypeFloat import ParamTypeFloat
from simple_serial_protocol.param_type.ParamTypeInt16 import ParamTypeInt16
from simple_serial_protocol.param_type.ParamTypeInt32 import ParamTypeInt32
from simple_serial_protocol.param_type.ParamTypeInt64 import ParamTypeInt64
from simple_serial_protocol.param_type.ParamTypeInt8 import ParamTypeInt8
from simple_serial_protocol.param_type.ParamTypeString import ParamTypeString
from simple_serial_protocol.param_type.ParamTypeUnsignedInt16 import ParamTypeUnsignedInt16
from simple_serial_protocol.param_type.ParamTypeUnsignedInt32 import ParamTypeUnsignedInt32
from simple_serial_protocol.param_type.ParamTypeUnsignedInt64 import ParamTypeUnsignedInt64
from simple_serial_protocol.param_type.ParamTypeUnsignedInt8 import ParamTypeUnsignedInt8
from simple_serial_protocol.serial_port.AbstractSerialPort import AbstractSerialPort
from simple_serial_protocol.serial_port.PySerialSerialPort import PySerialSerialPort


@dataclass(frozen=True, slots=True)
class CommandParam:
    type: str
    value: Any


class SimpleSerialProtocol:
    __CHAR_EOT: Final[Byte] = 0x0A  # End of Transmission - Line Feed Zeichen \n

    @overload
    def __init__(self, portname: str, baudrate: Baudrate, error_cb: ErrorCallback | None = None) -> None:
        pass

    @overload
    def __init__(self, serial_port_instance: AbstractSerialPort, error_cb: ErrorCallback | None = None):
        pass

    def __init__(
            self,
            portname_or_serial_port_instance: str | AbstractSerialPort,
            baudrate_or_error_cb: ErrorCallback | Baudrate | None = None,
            error_cb: ErrorCallback | None = None
    ):
        self.__serial_port: Final[AbstractSerialPort] = (
            portname_or_serial_port_instance
            if isinstance(portname_or_serial_port_instance, AbstractSerialPort)
            else PySerialSerialPort(str(portname_or_serial_port_instance), baudrate_or_error_cb)
        )
        self.__error_cb: ErrorCallback | None = (
            error_cb_or_baudrate
            if isinstance(portname_or_serial_port_instance, AbstractSerialPort)
            else error_cb
        )
        self.__is_initialized: bool = False
        self.__listener_thread: Thread | None = None
        self.__stop_event: Event | None = None
        self.__registered_commands: Final[dict[str, RegisteredCommand]] = {}
        self.__current_command: RegisteredCommand | None = None
        self.__param_type_instances: Final[dict[str, ParamType[Any]]] = {}
        self.__init_param_types()

    @property
    def is_open(self) -> bool:
        return self.__serial_port.is_open

    def init(self, initilizationDelay: float = 2.5):
        self.__serial_port.open()
        self.__stop_event = Event()
        self.__listener_thread = Thread(target=self.__serial_listener)
        self.__listener_thread.start()
        # TODO: make it non blocking
        sleep(initilizationDelay)
        self.__is_initialized = True

    def dispose(self):
        self.__is_initialized = False
        self.__stop_event.set()
        self.__listener_thread.join()
        self.__serial_port.close()
        self.__stop_event = None
        self.__listener_thread = None
        self.__registered_commands.clear()
        self.__error_cb = None

    def has_registered_command(self, command_id: str) -> None:
        return command_id in self.__registered_commands

    def registerCommand(self, command_id: str, callback: CommandCallback, param_types: list[str] = None):
        if self.has_registered_command(command_id):
            raise CommandAlreadyRegisteredException
        registered_command: RegisteredCommand = RegisteredCommand(command_id, callback, param_types)
        self.__registered_commands[command_id] = registered_command

    def unregisterCommand(self, command_id: str):
        if not self.has_registered_command(command_id):
            raise CommandIsNotRegisteredException
        command: RegisteredCommand = self.__registered_commands[command_id]
        command.dispose()
        del self.__registered_commands[command_id]

    def write_command(self, command_id: str, params: list[CommandParam] = None) -> None:
        command_id_byte: bytes = self.__param_type_instances.get(ParamTypeChar.NAME).get_buffer(command_id)
        self.__write(command_id_byte)
        if params is not None:
            for param in params:
                if ParamsParser.has_type(param.type):
                    typeClassInstance: ParamType[Any] = self.__param_type_instances.get(param.type)
                    buffer: bytes = typeClassInstance.get_buffer(param.value)
                    self.__write(buffer)
                else:
                    raise ParamTypeUnknownException
        eot_byte: bytes = self.__param_type_instances.get(ParamTypeInt8.NAME).get_buffer(
            SimpleSerialProtocol.__CHAR_EOT
        )
        self.__write(eot_byte)

    def __add_param_type(self, name: str, clazz: any) -> None:
        # if ParamsParser.has_type(name):
        #     raise ParamTypeIsAlreadyRegisteredException
        if not ParamsParser.has_type(name):
            ParamsParser.add_type(name, clazz)
        self.__param_type_instances[name] = clazz()

    def __serial_listener(self):
        while not self.__stop_event.is_set():
            if not self.__is_initialized:
                self.__serial_port.flush()
                continue
            if self.__serial_port.available() > 0:
                byte: Byte = self.__serial_port.read()
                self.__on_data(byte)

    def __write(self, buffer: bytes) -> None:
        self.__serial_port.write(buffer)

    def __init_param_types(self) -> None:
        self.__add_param_type(ParamTypeByte.NAME, ParamTypeByte)
        self.__add_param_type(ParamTypeBoolean.NAME, ParamTypeBoolean)
        self.__add_param_type(ParamTypeChar.NAME, ParamTypeChar)
        self.__add_param_type(ParamTypeString.NAME, ParamTypeString)
        self.__add_param_type(ParamTypeFloat.NAME, ParamTypeFloat)
        self.__add_param_type(ParamTypeInt8.NAME, ParamTypeInt8)
        self.__add_param_type(ParamTypeInt16.NAME, ParamTypeInt16)
        self.__add_param_type(ParamTypeInt32.NAME, ParamTypeInt32)
        self.__add_param_type(ParamTypeInt64.NAME, ParamTypeInt64)
        self.__add_param_type(ParamTypeUnsignedInt8.NAME, ParamTypeUnsignedInt8)
        self.__add_param_type(ParamTypeUnsignedInt16.NAME, ParamTypeUnsignedInt16)
        self.__add_param_type(ParamTypeUnsignedInt32.NAME, ParamTypeUnsignedInt32)
        self.__add_param_type(ParamTypeUnsignedInt64.NAME, ParamTypeUnsignedInt64)

    def __on_data(self, byte: Byte) -> None:
        # print('__on_data', byte)
        if self.__current_command is not None:
            # Got command already -> reading param data
            if self.__current_command.params_read():
                # Check EOT -> call callback
                if byte == SimpleSerialProtocol.__CHAR_EOT:
                    self.__current_command.call_callback()
                    self.__current_command = None
                else:
                    raise EotWasNotReadException
            else:
                self.__current_command.add_byte(byte)
        else:
            command_name: str = chr(byte)
            if command_name not in self.__registered_commands:
                # Command not found
                raise CommandIsNotRegisteredException(command_name)
            # New command -> Preparing buffer for reading
            self.__current_command = self.__registered_commands[command_name]
            self.__current_command.reset_param_parser()
