import csv
from datetime import datetime
from typing import List
import sqlite3

from chiccheap.repositories.produit_repo import ProduitRepository
from chiccheap.repositories.vente_repo import VenteRepository


class RapportService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.vente_repo = VenteRepository(conn)
        self.produit_repo = ProduitRepository(conn)

    def ventes_par_jour(self, debut: str, fin: str) -> List[sqlite3.Row]:
        return self.vente_repo.ventes_between(debut, fin)

    def top_produits(self, limit: int = 5):
        return self.vente_repo.top_products(limit)

    def export_ventes_csv(self, debut: str, fin: str, path: str) -> None:
        rows = self.ventes_par_jour(debut, fin)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'date', 'client_id', 'total_ht', 'taxe', 'remise_pct', 'total_ttc'])
            for r in rows:
                writer.writerow([
                    r['id'], r['date'], r['client_id'], r['total_ht'], r['taxe'], r['remise_pct'], r['total_ttc']
                ])

    def export_stock_csv(self, path: str) -> None:
        rows = self.produit_repo.list_all()
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nom', 'categorie', 'stock', 'seuil_alerte'])
            for r in rows:
                writer.writerow([r['id'], r['nom'], r['categorie'], r['stock'], r['seuil_alerte']])

    def periode_default(self) -> tuple[str, str]:
        now = datetime.now()
        debut = now.replace(day=1).strftime('%Y-%m-%d 00:00:00')
        fin = now.strftime('%Y-%m-%d 23:59:59')
        return debut, fin
