import sqlite3
from typing import List, Tuple, Optional

from chiccheap.repositories.produit_repo import ProduitRepository
from chiccheap.repositories.vente_repo import VenteRepository


class VenteService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.vente_repo = VenteRepository(conn)
        self.produit_repo = ProduitRepository(conn)

    def calculer_totaux(
        self, lignes: List[Tuple[int, int]], taxe: float, remise_pct: float
    ) -> Tuple[float, float]:
        # lignes: [(produit_id, qte)]
        total_ht = 0.0
        for prod_id, qte in lignes:
            prod = self.produit_repo.get(prod_id)
            if not prod:
                raise ValueError('Produit introuvable')
            total_ht += prod['prix'] * qte
        total_ht = round(total_ht * (1 - remise_pct), 2)
        total_ttc = round(total_ht * (1 + taxe), 2)
        return total_ht, total_ttc

    def enregistrer_vente(
        self, client_id: Optional[int], lignes: List[Tuple[int, int]], taxe: float, remise_pct: float
    ) -> int:
        total_ht, total_ttc = self.calculer_totaux(lignes, taxe, remise_pct)
        vente_id = self.vente_repo.insert_vente(client_id, total_ht, taxe, remise_pct, total_ttc)
        for prod_id, qte in lignes:
            prod = self.produit_repo.get(prod_id)
            prix_u = prod['prix']
            self.vente_repo.insert_ligne(vente_id, prod_id, qte, prix_u)
            self.produit_repo.update_stock(prod_id, -qte)
        return vente_id

    def ventes_par_periode(self, debut: str, fin: str):
        return self.vente_repo.ventes_between(debut, fin)

    def top_produits(self, limit: int = 5):
        return self.vente_repo.top_products(limit)
