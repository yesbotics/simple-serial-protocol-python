from typing import Callable, TypeAlias

Byte: TypeAlias = int
CommandCallback: TypeAlias = Callable[[Byte], None]
