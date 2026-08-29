from typing import List, Optional
import sqlite3

from chiccheap.models.produit import Produit


class ProduitRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_all(self) -> List[sqlite3.Row]:
        return self.conn.execute('SELECT * FROM produit').fetchall()

    def search(self, mot: str, categorie: Optional[str] = None) -> List[sqlite3.Row]:
        query = 'SELECT * FROM produit WHERE nom LIKE ?'
        params = [f'%{mot}%']
        if categorie:
            query += ' AND categorie = ?'
            params.append(categorie)
        return self.conn.execute(query, params).fetchall()

    def insert(self, produit: Produit) -> int:
        cur = self.conn.execute(
            '''
            INSERT INTO produit (nom, categorie, taille, couleur, prix, stock, seuil_alerte)
            VALUES (?,?,?,?,?,?,?)
            ''',
            (
                produit.nom,
                produit.categorie,
                produit.taille,
                produit.couleur,
                produit.prix,
                produit.stock,
                produit.seuil_alerte,
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def update(self, produit: Produit) -> None:
        self.conn.execute(
            '''
            UPDATE produit SET nom=?, categorie=?, taille=?, couleur=?, prix=?, stock=?, seuil_alerte=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            ''',
            (
                produit.nom,
                produit.categorie,
                produit.taille,
                produit.couleur,
                produit.prix,
                produit.stock,
                produit.seuil_alerte,
                produit.id,
            ),
        )
        self.conn.commit()

    def delete(self, produit_id: int) -> None:
        self.conn.execute('DELETE FROM produit WHERE id=?', (produit_id,))
        self.conn.commit()

    def get(self, produit_id: int) -> Optional[sqlite3.Row]:
        return self.conn.execute('SELECT * FROM produit WHERE id=?', (produit_id,)).fetchone()

    def update_stock(self, produit_id: int, delta: int) -> None:
        self.conn.execute(
            'UPDATE produit SET stock = stock + ?, updated_at=CURRENT_TIMESTAMP WHERE id=?',
            (delta, produit_id),
        )
        self.conn.commit()
