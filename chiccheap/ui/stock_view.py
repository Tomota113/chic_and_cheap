import tkinter as tk
from tkinter import ttk, messagebox

from chiccheap.db import get_connection
from chiccheap.services.produit_service import ProduitService
from chiccheap.services.stock_service import StockService


class StockView(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.conn = get_connection()
        self.produits = ProduitService(self.conn)
        self.service = StockService(self.conn)

        form = tk.Frame(self)
        form.pack(fill=tk.X, pady=5)
        tk.Label(form, text='Produit').grid(row=0, column=0, padx=5, pady=2)
        tk.Label(form, text='Type').grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form, text='Quantite').grid(row=0, column=2, padx=5, pady=2)
        tk.Label(form, text='Commentaire').grid(row=0, column=3, padx=5, pady=2)

        produits = self.produits.lister()
        self.prod_var = tk.StringVar()
        ttk.Combobox(
            form, textvariable=self.prod_var, values=[f"{p['id']} - {p['nom']}" for p in produits]
        ).grid(row=1, column=0, padx=5, pady=2)
        self.type_var = tk.StringVar(value='ENTREE')
        ttk.Combobox(form, textvariable=self.type_var, values=['ENTREE', 'SORTIE']).grid(
            row=1, column=1, padx=5, pady=2
        )
        self.qte_var = tk.StringVar(value='1')
        tk.Entry(form, textvariable=self.qte_var, width=8).grid(row=1, column=2, padx=5, pady=2)
        self.comment_var = tk.Entry(form, width=30)
        self.comment_var.grid(row=1, column=3, padx=5, pady=2)
        tk.Button(form, text='Valider', command=self.valider).grid(row=1, column=4, padx=5)

        self.table = ttk.Treeview(self, columns=('produit_id', 'type', 'quantite', 'date'), show='headings')
        for col in ('produit_id', 'type', 'quantite', 'date'):
            self.table.heading(col, text=col.upper())
        self.table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh()

    def refresh(self) -> None:
        self.table.delete(*self.table.get_children())
        for mv in self.service.historique():
            self.table.insert('', tk.END, values=(mv['produit_id'], mv['type'], mv['quantite'], mv['date']))

    def valider(self) -> None:
        if not self.prod_var.get():
            return
        try:
            prod_id = int(self.prod_var.get().split(' - ')[0])
            qte = int(self.qte_var.get())
        except ValueError:
            messagebox.showerror('Erreur', 'Quantite invalide.')
            return
        try:
            self.service.mouvement(prod_id, self.type_var.get(), qte, self.comment_var.get())
        except Exception as exc:
            messagebox.showerror('Erreur', str(exc))
            return
        self.refresh()
        messagebox.showinfo('OK', 'Mouvement enregistre.')
