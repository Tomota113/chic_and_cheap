from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'db.sqlite3'
LOG_PATH = BASE_DIR / 'app.log'

THEME_BG = '#fdf8f1'
THEME_ACCENT = '#c9a227'
THEME_TEXT = '#1f1a17'
DEFAULT_TAXE = 0.18
DEFAULT_DEVISE = 'FCFA'
