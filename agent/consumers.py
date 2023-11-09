from typing import Dict, Protocol

class Consumer(Protocol):
    def __init__(self) -> None:
        pass
    
    def receive(self, message: Dict[str, str]) -> None:
        pass
    
    
