import logging
import sqlite3
from typing import Iterable

from chiccheap.config import DB_PATH, LOG_PATH, DEFAULT_TAXE, DEFAULT_DEVISE

logger = logging.getLogger('chiccheap')


def _setup_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_PATH, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


DDL_STATEMENTS: Iterable[str] = (
    '''
    CREATE TABLE IF NOT EXISTS utilisateur (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nom TEXT UNIQUE NOT NULL,
      role TEXT NOT NULL CHECK(role IN ('GERANT','VENDEUR','STOCK')),
      hash_mdp TEXT NOT NULL,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS produit (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nom TEXT NOT NULL,
      categorie TEXT NOT NULL,
      taille TEXT,
      couleur TEXT,
      prix REAL NOT NULL CHECK(prix>=0),
      stock INTEGER NOT NULL DEFAULT 0,
      seuil_alerte INTEGER NOT NULL DEFAULT 5,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS client (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nom TEXT NOT NULL,
      telephone TEXT,
      email TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS fournisseur (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nom TEXT NOT NULL,
      telephone TEXT,
      note TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS vente (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      client_id INTEGER,
      total_ht REAL NOT NULL DEFAULT 0,
      taxe REAL NOT NULL DEFAULT 0,
      remise_pct REAL NOT NULL DEFAULT 0,
      total_ttc REAL NOT NULL DEFAULT 0,
      FOREIGN KEY(client_id) REFERENCES client(id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS ligne_vente (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      vente_id INTEGER NOT NULL,
      produit_id INTEGER NOT NULL,
      qte INTEGER NOT NULL CHECK(qte>0),
      prix_unitaire REAL NOT NULL CHECK(prix_unitaire>=0),
      FOREIGN KEY(vente_id) REFERENCES vente(id),
      FOREIGN KEY(produit_id) REFERENCES produit(id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS mouvement_stock (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      produit_id INTEGER NOT NULL,
      type TEXT NOT NULL CHECK(type IN ('ENTREE','SORTIE')),
      quantite INTEGER NOT NULL CHECK(quantite>0),
      date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      commentaire TEXT,
      FOREIGN KEY(produit_id) REFERENCES produit(id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS parametre (
      cle TEXT PRIMARY KEY,
      valeur TEXT NOT NULL
    );
    ''',
)


def init_db() -> None:
    _setup_logging()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cur = conn.cursor()
    for stmt in DDL_STATEMENTS:
        cur.execute(stmt)
    conn.commit()
    seed_data(conn)
    conn.close()
    logger.info('Base initialisee.')


def seed_data(conn: sqlite3.Connection) -> None:
    from chiccheap.utils.hashing import hash_password

    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM utilisateur;')
    if cur.fetchone()[0] == 0:
        users = [
            ('admin', 'GERANT', hash_password('admin123')),
            ('aminata', 'VENDEUR', hash_password('1234')),
            ('assan', 'STOCK', hash_password('1234')),
        ]
        cur.executemany('INSERT INTO utilisateur (nom, role, hash_mdp) VALUES (?,?,?)', users)
    cur.execute('SELECT COUNT(*) FROM produit;')
    if cur.fetchone()[0] == 0:
        produits = [
            ('Robe Ankara', 'Femme', 'M', 'Rouge', 25000, 12, 5),
            ('Boubou', 'Homme', 'L', 'Bleu', 30000, 7, 5),
            ('Casquette Wax', 'Accessoire', '', 'Marron', 10000, 20, 5),
        ]
        cur.executemany('''
            INSERT INTO produit (nom, categorie, taille, couleur, prix, stock, seuil_alerte)
            VALUES (?,?,?,?,?,?,?)
        ''', produits)
    cur.execute('SELECT COUNT(*) FROM client;')
    if cur.fetchone()[0] == 0:
        clients = [
            ('Awa Traore', '77 00 00 00', None),
            ('Moussa Diarra', '76 11 22 33', None),
        ]
        cur.executemany('INSERT INTO client (nom, telephone, email) VALUES (?,?,?)', clients)
    cur.execute('SELECT COUNT(*) FROM parametre;')
    if cur.fetchone()[0] == 0:
        params = [('taxe', str(DEFAULT_TAXE)), ('devise', DEFAULT_DEVISE)]
        cur.executemany('INSERT INTO parametre (cle, valeur) VALUES (?,?)', params)
    conn.commit()
