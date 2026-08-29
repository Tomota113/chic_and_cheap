from dataclasses import dataclass
from typing import Optional


@dataclass
class LigneVente:
    id: Optional[int]
    vente_id: int
    produit_id: int
    qte: int
    prix_unitaire: float
