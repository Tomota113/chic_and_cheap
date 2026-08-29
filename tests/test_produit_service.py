from chiccheap.db import get_connection, init_db
from chiccheap.models.produit import Produit
from chiccheap.services.produit_service import ProduitService


def setup_module():
    init_db()


def test_ajouter_modifie_supprimer(tmp_path, monkeypatch):
    from chiccheap import db

    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'test.sqlite3')
    db.init_db()
    conn = get_connection()
    service = ProduitService(conn)
    pid = service.ajouter(
        Produit(id=None, nom='Test', categorie='Homme', taille='L', couleur='Noir', prix=1000, stock=5)
    )
    produit = service.repo.get(pid)
    assert produit['nom'] == 'Test'
    produit_obj = Produit(
        id=pid, nom='Test2', categorie='Homme', taille='L', couleur='Noir', prix=1200, stock=4
    )
    service.modifier(produit_obj)
    assert service.repo.get(pid)['nom'] == 'Test2'
    service.supprimer(pid)
    assert service.repo.get(pid) is None
