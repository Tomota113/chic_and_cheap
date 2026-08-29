from dataclasses import dataclass
from typing import Optional


@dataclass
class Produit:
    id: Optional[int]
    nom: str
    categorie: str
    taille: str
    couleur: str
    prix: float
    stock: int
    seuil_alerte: int = 5
