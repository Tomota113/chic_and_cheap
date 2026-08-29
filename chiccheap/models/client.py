from dataclasses import dataclass
from typing import Optional


@dataclass
class Client:
    id: Optional[int]
    nom: str
    telephone: str
    email: Optional[str] = None
