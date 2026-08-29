from typing import Optional
import sqlite3


class UtilisateurRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_by_name(self, nom: str) -> Optional[sqlite3.Row]:
        return self.conn.execute('SELECT * FROM utilisateur WHERE nom=?', (nom,)).fetchone()

    def reset_password(self, user_id: int, new_hash: str) -> None:
        self.conn.execute('UPDATE utilisateur SET hash_mdp=? WHERE id=?', (new_hash, user_id))
        self.conn.commit()

    def list_all(self):
        return self.conn.execute('SELECT * FROM utilisateur').fetchall()
