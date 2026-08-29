from typing import List
import sqlite3


class ClientRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_all(self) -> List[sqlite3.Row]:
        return self.conn.execute('SELECT * FROM client').fetchall()
