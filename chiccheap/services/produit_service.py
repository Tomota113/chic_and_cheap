import sqlite3
from typing import List, Optional

from chiccheap.models.produit import Produit
from chiccheap.repositories.produit_repo import ProduitRepository


class ProduitService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.repo = ProduitRepository(conn)

    def lister(self) -> List[sqlite3.Row]:
        return self.repo.list_all()

    def rechercher(self, mot: str, categorie: Optional[str] = None) -> List[sqlite3.Row]:
        return self.repo.search(mot, categorie)

    def ajouter(self, produit: Produit) -> int:
        return self.repo.insert(produit)

    def modifier(self, produit: Produit) -> None:
        self.repo.update(produit)

    def supprimer(self, produit_id: int) -> None:
        self.repo.delete(produit_id)

    def produits_en_alerte(self) -> List[sqlite3.Row]:
        return [
            row
            for row in self.repo.list_all()
            if row['stock'] < row['seuil_alerte']
        ]
