from chiccheap.db import init_db, get_connection
from chiccheap.services.rapport_service import RapportService


def test_export_csv(tmp_path, monkeypatch):
    from chiccheap import db

    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'rapport.sqlite3')
    init_db()
    conn = get_connection()
    service = RapportService(conn)
    debut, fin = service.periode_default()
    path = tmp_path / 'ventes.csv'
    service.export_ventes_csv(debut, fin, path)
    assert path.exists()
