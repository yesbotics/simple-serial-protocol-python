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
    ParamTypeUnknownException, SimpleSerialException
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
        self._serial_port: Final[AbstractSerialPort] = (
            portname_or_serial_port_instance
            if isinstance(portname_or_serial_port_instance, AbstractSerialPort)
            else PySerialSerialPort(str(portname_or_serial_port_instance), baudrate_or_error_cb)
        )
        self._error_cb: ErrorCallback | None = error_cb
        self._is_initialized: bool = False
        self._listener_thread: Thread | None = None
        self._stop_event: Event | None = None
        self._registered_commands: Final[dict[str, RegisteredCommand]] = {}
        self._current_command: RegisteredCommand | None = None
        self._param_type_instances: Final[dict[str, ParamType[Any]]] = {}
        self._init_param_types()

    @property
    def is_open(self) -> bool:
        return self._serial_port.is_open

    def init(self, initilizationDelay: float = 2.5):
        self._serial_port.open()
        self._stop_event = Event()
        self._listener_thread = Thread(target=self._serial_listener)
        self._listener_thread.start()
        # TODO: make it non blocking?
        sleep(initilizationDelay)
        self._is_initialized = True

    def dispose(self):
        self._is_initialized = False
        if self._stop_event is not None:
            self._stop_event.set()
        if self._listener_thread is not None:
            self._listener_thread.join()
        self._serial_port.close()
        for key, item in self._registered_commands.items():
            item.dispose()
        self._registered_commands.clear()
        self._stop_event = None
        self._listener_thread = None
        self._error_cb = None

    def has_registered_command(self, command_id: str) -> bool:
        return command_id in self._registered_commands

    def register_command(self, command_id: str, callback: CommandCallback, param_types: list[str] = None):
        if self.has_registered_command(command_id):
            raise CommandAlreadyRegisteredException
        registered_command: RegisteredCommand = RegisteredCommand(command_id, callback, param_types)
        self._registered_commands[command_id] = registered_command

    def unregister_command(self, command_id: str):
        if not self.has_registered_command(command_id):
            raise CommandIsNotRegisteredException
        command: RegisteredCommand = self._registered_commands[command_id]
        command.dispose()
        del self._registered_commands[command_id]

    def write_command(self, command_id: str, params: list[CommandParam] = None) -> None:
        command_id_byte: bytes = self._param_type_instances.get(ParamTypeChar.NAME).get_buffer(command_id)
        self._write(command_id_byte)
        if params is not None:
            for param in params:
                if ParamsParser.has_type(param.type):
                    typeClassInstance: ParamType[Any] = self._param_type_instances.get(param.type)
                    buffer: bytes = typeClassInstance.get_buffer(param.value)
                    self._write(buffer)
                else:
                    raise ParamTypeUnknownException
        eot_byte: bytes = self._param_type_instances.get(ParamTypeInt8.NAME).get_buffer(
            SimpleSerialProtocol.__CHAR_EOT
        )
        self._write(eot_byte)

    def _add_param_type(self, name: str, clazz: any) -> None:
        # if ParamsParser.has_type(name):
        #     raise ParamTypeIsAlreadyRegisteredException
        if not ParamsParser.has_type(name):
            ParamsParser.add_type(name, clazz)
        self._param_type_instances[name] = clazz()

    def _serial_listener(self) -> None:
        try:
            while not self._stop_event.is_set():
                if not self._is_initialized:
                    self._serial_port.flush()
                    continue
                if self._serial_port.available() > 0:
                    byte: Byte = self._serial_port.read()
                    self._on_data(byte)
        except OSError as e:
            # print('SimpleSerialException', e)
            self._is_initialized = False
            self._stop_event.set()
            self._stop_event = None
            self._listener_thread = None
            self._registered_commands.clear()
            if self._error_cb is not None:
                self._error_cb(e)
            self._error_cb = None

    def _write(self, buffer: bytes) -> None:
        # print("_write:", buffer)
        self._serial_port.write(buffer)

    def _init_param_types(self) -> None:
        self._add_param_type(ParamTypeByte.NAME, ParamTypeByte)
        self._add_param_type(ParamTypeBoolean.NAME, ParamTypeBoolean)
        self._add_param_type(ParamTypeChar.NAME, ParamTypeChar)
        self._add_param_type(ParamTypeString.NAME, ParamTypeString)
        self._add_param_type(ParamTypeFloat.NAME, ParamTypeFloat)
        self._add_param_type(ParamTypeInt8.NAME, ParamTypeInt8)
        self._add_param_type(ParamTypeInt16.NAME, ParamTypeInt16)
        self._add_param_type(ParamTypeInt32.NAME, ParamTypeInt32)
        self._add_param_type(ParamTypeInt64.NAME, ParamTypeInt64)
        self._add_param_type(ParamTypeUnsignedInt8.NAME, ParamTypeUnsignedInt8)
        self._add_param_type(ParamTypeUnsignedInt16.NAME, ParamTypeUnsignedInt16)
        self._add_param_type(ParamTypeUnsignedInt32.NAME, ParamTypeUnsignedInt32)
        self._add_param_type(ParamTypeUnsignedInt64.NAME, ParamTypeUnsignedInt64)

    def _on_data(self, byte: Byte) -> None:
        # print('_on_data', byte)
        if self._current_command is not None:
            # Got command already -> reading param data
            if self._current_command.params_read():
                # Check EOT -> call callback
                if byte == SimpleSerialProtocol.__CHAR_EOT:
                    self._current_command.call_callback()
                    self._current_command = None
                else:
                    raise EotWasNotReadException
            else:
                self._current_command.add_byte(byte)
        else:
            command_name: str = chr(byte)
            if command_name not in self._registered_commands:
                # Command not found
                raise CommandIsNotRegisteredException(command_name)
            # New command -> Preparing buffer for reading
            self._current_command = self._registered_commands[command_name]
            self._current_command.reset_param_parser()
