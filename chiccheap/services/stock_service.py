import sqlite3
from typing import List

from chiccheap.repositories.stock_repo import StockRepository


class StockService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.repo = StockRepository(conn)

    def mouvement(self, produit_id: int, type_mv: str, quantite: int, commentaire: str = '') -> None:
        if type_mv not in {'ENTREE', 'SORTIE'}:
            raise ValueError('Type de mouvement invalide')
        self.repo.add_mouvement(produit_id, type_mv, quantite, commentaire)

    def historique(self) -> List[sqlite3.Row]:
        return self.repo.history()
