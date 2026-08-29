from typing import List, Optional
import sqlite3


class VenteRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def insert_vente(self, client_id: Optional[int], total_ht: float, taxe: float, remise_pct: float, total_ttc: float) -> int:
        cur = self.conn.execute(
            '''
            INSERT INTO vente (client_id, total_ht, taxe, remise_pct, total_ttc)
            VALUES (?,?,?,?,?)
            ''',
            (client_id, total_ht, taxe, remise_pct, total_ttc),
        )
        self.conn.commit()
        return cur.lastrowid

    def insert_ligne(self, vente_id: int, produit_id: int, qte: int, prix_unitaire: float) -> None:
        self.conn.execute(
            '''
            INSERT INTO ligne_vente (vente_id, produit_id, qte, prix_unitaire)
            VALUES (?,?,?,?)
            ''',
            (vente_id, produit_id, qte, prix_unitaire),
        )
        self.conn.commit()

    def ventes_between(self, start: str, end: str) -> List[sqlite3.Row]:
        return self.conn.execute(
            'SELECT * FROM vente WHERE date BETWEEN ? AND ? ORDER BY date ASC', (start, end)
        ).fetchall()

    def top_products(self, limit: int = 5) -> List[sqlite3.Row]:
        return self.conn.execute(
            '''
            SELECT produit_id, SUM(qte) AS total_qte
            FROM ligne_vente
            GROUP BY produit_id
            ORDER BY total_qte DESC
            LIMIT ?
            ''',
            (limit,),
        ).fetchall()
