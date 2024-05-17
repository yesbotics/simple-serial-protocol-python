from typing import Callable, TypeAlias

Byte: TypeAlias = int
CommandCallback: TypeAlias = Callable[..., None]
ErrorCallback: TypeAlias = Callable[[Exception], None]
