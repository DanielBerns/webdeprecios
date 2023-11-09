from typing import Generator, Protocol

class Producer(Protocol):
    def __init__(self) -> None:
        pass
    
    def content(self) -> Generator[str, None, None]:
        yield from ()
