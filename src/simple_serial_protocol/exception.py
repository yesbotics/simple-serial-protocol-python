from typing import Final


class SimpleSerialException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: Final[str] = msg


class CommandAlreadyRegisteredException(SimpleSerialException):
    def __init__(self, cmd: str) -> None:
        super().__init__('ERROR_COMMAND_IS_ALREADY_REGISTERED')


class CommandIsNotRegisteredException(SimpleSerialException):
    def __init__(self, command: str) -> None:
        super().__init__(f'ERROR_COMMAND_IS_NOT_REGISTERED: {command}')


class IsNotEotException(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_IS_NOT_EOT')


class EotWasNotReadException(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_EOT_WAS_NOT_READ')


class ParamTypeUnknownException(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_PARAM_TYPE_UNKNOWN')


class UnknownException(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('UNKNOWN')


class WrongCommandNameLengthException(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_WRONG_COMMAND_NAME_LENGTH')


class ParamTypeIsAlreadyRegisteredException(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_PARAM_TYPE_IS_ALREADY_REGISTERED')


class ParserTooManyBytesException(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__(
            'ERROR_PARSER_TOO_MANY_BYTES, Tried to add byte to param parser but all types filled.'
        )
