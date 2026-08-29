from chiccheap import db


def test_init_db_creates_tables(tmp_path, monkeypatch):
    db_path = tmp_path / 'db.sqlite3'
    monkeypatch.setattr(db, 'DB_PATH', db_path)
    db.init_db()
    assert db_path.exists()
    conn = db.get_connection()
    tables = {r[0] for r in conn.execute('SELECT name FROM sqlite_master')}
    assert 'produit' in tables and 'utilisateur' in tables
