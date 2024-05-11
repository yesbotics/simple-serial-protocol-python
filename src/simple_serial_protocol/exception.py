from typing import Final


class SimpleSerialException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: Final[str] = msg


class CommandAlreadyRegisteredException(SimpleSerialException):
    def __init__(self, cmd: str) -> None:
        super().__init__('ERROR_COMMAND_IS_ALREADY_REGISTERED')


class CommandIsNotRegisteredexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_COMMAND_IS_NOT_REGISTERED')


class IsNotEotexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_IS_NOT_EOT')


class EotWasNotReadexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_EOT_WAS_NOT_READ')


class ParamTypeUnknownexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_PARAM_TYPE_UNKNOWN')


class Unknownexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('UNKNOWN')


class WrongCommandNameLengthexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_WRONG_COMMAND_NAME_LENGTH')


class ParamTypeIsAlreadyRegisteredexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_PARAM_TYPE_IS_ALREADY_REGISTERED')


class ParserTooManyBytesexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_PARSER_TOO_MANY_BYTES')


class CallbackIsNullexception(SimpleSerialException):
    def __init__(self) -> None:
        super().__init__('ERROR_CALLBACK_IS_NULL')
