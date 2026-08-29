from dataclasses import dataclass
from typing import Optional


@dataclass
class MouvementStock:
    id: Optional[int]
    produit_id: int
    type: str  # ENTREE | SORTIE
    quantite: int
    commentaire: str
