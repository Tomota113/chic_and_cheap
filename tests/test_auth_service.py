from chiccheap.db import init_db, get_connection
from chiccheap.services.auth_service import AuthService


def test_authenticate_success(tmp_path, monkeypatch):
    from chiccheap import db

    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'auth.sqlite3')
    init_db()
    conn = get_connection()
    service = AuthService(conn)
    assert service.authenticate('admin', 'admin123') == 'GERANT'
    assert service.authenticate('admin', 'wrong') is None
