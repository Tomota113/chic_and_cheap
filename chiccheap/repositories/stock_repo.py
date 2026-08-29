import sqlite3
from typing import List


class StockRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def add_mouvement(self, produit_id: int, type_mv: str, quantite: int, commentaire: str) -> None:
        self.conn.execute(
            '''
            INSERT INTO mouvement_stock (produit_id, type, quantite, commentaire)
            VALUES (?,?,?,?)
            ''',
            (produit_id, type_mv, quantite, commentaire),
        )
        delta = quantite if type_mv == 'ENTREE' else -quantite
        self.conn.execute(
            'UPDATE produit SET stock = stock + ?, updated_at=CURRENT_TIMESTAMP WHERE id=?',
            (delta, produit_id),
        )
        self.conn.commit()

    def history(self, limit: int = 50) -> List[sqlite3.Row]:
        return self.conn.execute(
            'SELECT * FROM mouvement_stock ORDER BY date DESC LIMIT ?', (limit,)
        ).fetchall()
