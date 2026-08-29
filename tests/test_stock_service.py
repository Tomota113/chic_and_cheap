from chiccheap.db import init_db, get_connection
from chiccheap.services.stock_service import StockService


def test_mouvement_entree_sortie(tmp_path, monkeypatch):
    from chiccheap import db

    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'stock.sqlite3')
    init_db()
    conn = get_connection()
    service = StockService(conn)
    prod = conn.execute('SELECT id, stock FROM produit LIMIT 1').fetchone()
    service.mouvement(prod['id'], 'ENTREE', 3, 'test')
    stock = conn.execute('SELECT stock FROM produit WHERE id=?', (prod['id'],)).fetchone()[0]
    assert stock == prod['stock'] + 3
    service.mouvement(prod['id'], 'SORTIE', 2, 'test')
    stock2 = conn.execute('SELECT stock FROM produit WHERE id=?', (prod['id'],)).fetchone()[0]
    assert stock2 == prod['stock'] + 1
