import tkinter as tk
from tkinter import ttk, messagebox

from chiccheap.config import DEFAULT_TAXE
from chiccheap.db import get_connection
from chiccheap.services.produit_service import ProduitService
from chiccheap.services.vente_service import VenteService


class VentesView(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.conn = get_connection()
        self.produit_service = ProduitService(self.conn)
        self.vente_service = VenteService(self.conn)
        self.lignes = []  # [(prod_id, qte)]

        form = tk.Frame(self)
        form.pack(fill=tk.X, pady=5)
        tk.Label(form, text='Produit').grid(row=0, column=0, padx=5, pady=2)
        tk.Label(form, text='Quantite').grid(row=0, column=1, padx=5, pady=2)
        self.prod_var = tk.StringVar()
        self.qte_var = tk.StringVar(value='1')
        produits = self.produit_service.lister()
        self.prod_combo = ttk.Combobox(
            form, textvariable=self.prod_var, values=[f"{p['id']} - {p['nom']}" for p in produits]
        )
        self.prod_combo.grid(row=1, column=0, padx=5, pady=2)
        tk.Entry(form, textvariable=self.qte_var, width=8).grid(row=1, column=1, padx=5, pady=2)
        tk.Button(form, text='Ajouter ligne', command=self.ajouter_ligne).grid(
            row=1, column=2, padx=5, pady=2
        )

        self.table = ttk.Treeview(self, columns=('id', 'nom', 'qte', 'prix', 'total'), show='headings')
        for col in ('id', 'nom', 'qte', 'prix', 'total'):
            self.table.heading(col, text=col.upper())
        self.table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        actions = tk.Frame(self)
        actions.pack(fill=tk.X, pady=5)
        tk.Label(actions, text='Remise %').pack(side=tk.LEFT, padx=5)
        self.remise_var = tk.StringVar(value='0')
        tk.Entry(actions, textvariable=self.remise_var, width=6).pack(side=tk.LEFT)
        tk.Button(actions, text='Enregistrer la vente', command=self.enregistrer).pack(
            side=tk.LEFT, padx=10
        )
        tk.Button(actions, text='Annuler', command=self.annuler).pack(side=tk.LEFT)

        self.total_label = tk.Label(self, text='Total TTC: 0')
        self.total_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def ajouter_ligne(self) -> None:
        if not self.prod_var.get():
            return
        try:
            prod_id = int(self.prod_var.get().split(' - ')[0])
            qte = int(self.qte_var.get())
        except ValueError:
            messagebox.showerror('Erreur', 'Quantite invalide.')
            return
        prod = self.produit_service.repo.get(prod_id)
        if not prod:
            return
        self.lignes.append((prod_id, qte))
        total = prod['prix'] * qte
        self.table.insert('', tk.END, values=(prod['id'], prod['nom'], qte, prod['prix'], total))
        self._update_total()

    def _update_total(self) -> None:
        remise = float(self.remise_var.get() or 0) / 100
        total_ht, total_ttc = self.vente_service.calculer_totaux(self.lignes, DEFAULT_TAXE, remise)
        self.total_label.config(text=f'Total TTC: {total_ttc:.2f}')

    def enregistrer(self) -> None:
        try:
            remise = float(self.remise_var.get() or 0) / 100
        except ValueError:
            messagebox.showerror('Erreur', 'Remise invalide.')
            return
        try:
            vente_id = self.vente_service.enregistrer_vente(None, self.lignes, DEFAULT_TAXE, remise)
        except Exception as exc:
            messagebox.showerror('Erreur', str(exc))
            return
        messagebox.showinfo('Succes', f'Vente #{vente_id} enregistree.')
        self.annuler()

    def annuler(self) -> None:
        self.lignes = []
        self.table.delete(*self.table.get_children())
        self.remise_var.set('0')
        self._update_total()
