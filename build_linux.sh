#!/bin/bash
set -e
echo "Installation des dépendances..."
pip install -r requirements.txt pyinstaller
echo "Compilation de l'exécutable autonome Linux..."
pyinstaller --noconfirm --clean --onefile --name ChicAndCheap --add-data "chiccheap:chiccheap" app.py
echo "Succès ! Binaire disponible dans dist/ChicAndCheap"
