from dataclasses import dataclass
from typing import Optional


@dataclass
class Utilisateur:
    id: Optional[int]
    nom: str
    role: str
    hash_mdp: str
