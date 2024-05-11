from threading import Event, Thread
from typing import Callable, Final

from simple_serial_protocol.Baudrate import Baudrate
from simple_serial_protocol.AbstractSerialPort import AbstractSerialPort
from simple_serial_protocol.PySerialSerialPort import PySerialSerialPort
from simple_serial_protocol.PySide6SerialPort import PySide6SerialPort
from simple_serial_protocol.common import Byte, CommandCallback
from simple_serial_protocol.exception import CommandAlreadyRegisteredException


class SimpleSerialProtocol:

    @staticmethod
    def __create_serialport(
            portname: str,
            baudrate: Baudrate,
    ) -> AbstractSerialPort:
        try:
            import serial
            return PySerialSerialPort(portname, baudrate)
        except ImportError:
            pass
        try:
            import PySide6
            return PySide6SerialPort(portname, baudrate)
        except ImportError:
            pass
        raise RuntimeError('No serial port library like pyserial could be found')

    def __init__(self, portname: str, baudrate: Baudrate):
        self.__serial_port: Final[AbstractSerialPort] = SimpleSerialProtocol.__create_serialport(
            str(portname),
            baudrate
        )
        self.__listener_thread: Thread | None = None
        self.__stop_event: Event | None = None
        self.__registered_commands: Final[dict[Byte, CommandCallback]] = {}

    def init(self):
        self.__serial_port.open()
        self.__stop_event = Event()
        self.__listener_thread = Thread(target=self.__serial_listener)
        self.__listener_thread.start()

    def dispose(self):
        self.__stop_event.set()
        self.__listener_thread.join()
        self.__serial_port.close()
        self.__stop_event = None
        self.__listener_thread = None

    def registerCommand(self, command_id: Byte, callback: CommandCallback):
        if command_id in self.__registered_commands:
            raise CommandAlreadyRegisteredException
        self.__registered_commands[command_id] = callback

    def unregisterCommand(self, command_id: Byte):
        if command_id in self.__registered_commands:
            del self.__registered_commands[command_id]

    def __serial_listener(self):
        while not self.__stop_event.is_set():
            if self.__serial_port.available() > 0:
                byte: Byte = self.__serial_port.read()
                print(byte)
