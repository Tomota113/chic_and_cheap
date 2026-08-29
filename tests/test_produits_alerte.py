from chiccheap.db import init_db, get_connection
from chiccheap.services.produit_service import ProduitService
from chiccheap.models.produit import Produit


def test_produits_en_alerte(tmp_path, monkeypatch):
    from chiccheap import db

    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'alerte.sqlite3')
    init_db()
    conn = get_connection()
    service = ProduitService(conn)
    service.ajouter(
        Produit(id=None, nom='StockBas', categorie='Femme', taille='S', couleur='Rouge', prix=10, stock=1, seuil_alerte=5)
    )
    alerts = service.produits_en_alerte()
    assert any(p['nom'] == 'StockBas' for p in alerts)
