import tkinter as tk
from tkinter import ttk

from chiccheap.config import THEME_BG, THEME_TEXT
from chiccheap.ui.produits_view import ProduitsView
from chiccheap.ui.ventes_view import VentesView
from chiccheap.ui.stock_view import StockView
from chiccheap.ui.rapports_view import RapportsView
from chiccheap.ui.params_view import ParamsView


class MainWindow(tk.Toplevel):
    def __init__(self, master: tk.Misc, username: str, role: str):
        super().__init__(master)
        self.title(f'Chic and Cheap - Connecte en {username} ({role})')
        self.configure(bg=THEME_BG)
        self.geometry('1100x700')
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        notebook.add(ProduitsView(notebook), text='Produits')
        notebook.add(VentesView(notebook), text='Ventes')
        notebook.add(StockView(notebook), text='Stock')
        notebook.add(RapportsView(notebook), text='Rapports')
        notebook.add(ParamsView(notebook), text='Parametres')

        footer = tk.Label(self, text='Chic and Cheap', bg=THEME_BG, fg=THEME_TEXT)
        footer.pack(side=tk.BOTTOM, pady=5)
