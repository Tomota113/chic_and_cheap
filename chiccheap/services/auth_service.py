import sqlite3
from typing import Optional

from chiccheap.repositories.utilisateur_repo import UtilisateurRepository
from chiccheap.utils.hashing import verify_password


class AuthService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.repo = UtilisateurRepository(conn)

    def authenticate(self, username: str, password: str) -> Optional[str]:
        user = self.repo.get_by_name(username)
        if not user:
            return None
        if verify_password(password, user['hash_mdp']):
            return user['role']
        return None
