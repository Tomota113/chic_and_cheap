# Chic and Cheap

Application de bureau Tkinter pour gerer une boutique de vetements (produits, ventes, stock, rapports). DB SQLite locale avec initialisation automatique et donnees de demo.

## Prerequis
- Python 3.11+
- Windows (pour le .exe), mais l'appli tourne partout ou Tkinter est dispo.

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate  # ou source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer l'appli
```bash
python app.py
```
Identifiants demo : `admin / admin123`.

## Tests
```bash
pytest
```

## Packaging .exe
```bash
build_exe.bat
```
L'executable apparait dans `dist/ChicAndCheap.exe`.

## Arborescence
```
chic_and_cheap/
  app.py
  requirements.txt
  README.md
  pyproject.toml
  build_exe.bat
  chiccheap/
    ...
  tests/
    ...
```

## Captures d'ecran
Placeholders : docs/screens/login.png, docs/screens/main.png (a ajouter apres build).

## Notes
- Logs dans app.log.
- DB locale db.sqlite3 creee au premier lancement avec seed (utilisateurs, produits, clients, parametres).
- Code tape et commente en francais, conforme PEP8.
