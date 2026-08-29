from dataclasses import dataclass
from typing import Optional


@dataclass
class Fournisseur:
    id: Optional[int]
    nom: str
    telephone: str
    note: Optional[str] = None
