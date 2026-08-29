from chiccheap.db import init_db, get_connection
from chiccheap.services.vente_service import VenteService


def test_enregistrer_vente_met_a_jour_stock(tmp_path, monkeypatch):
    from chiccheap import db

    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'vente.sqlite3')
    init_db()
    conn = get_connection()
    service = VenteService(conn)
    prod = conn.execute('SELECT id, stock FROM produit LIMIT 1').fetchone()
    lignes = [(prod['id'], 1)]
    vente_id = service.enregistrer_vente(None, lignes, 0.18, 0)
    assert vente_id > 0
    new_stock = conn.execute('SELECT stock FROM produit WHERE id=?', (prod['id'],)).fetchone()[0]
    assert new_stock == prod['stock'] - 1
