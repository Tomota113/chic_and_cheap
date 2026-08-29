@echo off
py -m pip install -r requirements.txt
py -m PyInstaller --noconfirm --onefile --name ChicAndCheap app.py
