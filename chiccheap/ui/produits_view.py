import tkinter as tk
from tkinter import ttk, messagebox

from chiccheap.db import get_connection
from chiccheap.models.produit import Produit
from chiccheap.services.produit_service import ProduitService
from chiccheap.ui.widgets.search_bar import SearchBar
from chiccheap.ui.widgets.table_view import TableView


class ProduitsView(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.conn = get_connection()
        self.service = ProduitService(self.conn)

        toolbar = tk.Frame(self)
        toolbar.pack(fill=tk.X, pady=5)
        SearchBar(toolbar, self._on_search).pack(fill=tk.X, expand=True, padx=5)

        btns = tk.Frame(self)
        btns.pack(fill=tk.X, pady=5)
        tk.Button(btns, text='Ajouter', command=self._ajouter).pack(side=tk.LEFT, padx=4)
        tk.Button(btns, text='Modifier', command=self._modifier).pack(side=tk.LEFT, padx=4)
        tk.Button(btns, text='Supprimer', command=self._supprimer).pack(side=tk.LEFT, padx=4)

        self.table = TableView(
            self,
            columns=['id', 'nom', 'categorie', 'prix', 'stock', 'seuil_alerte'],
            height=18,
        )
        self.table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh()

    def refresh(self) -> None:
        rows = self.service.lister()
        display = [
            (r['id'], r['nom'], r['categorie'], r['prix'], r['stock'], r['seuil_alerte'])
            for r in rows
        ]
        self.table.populate(display)

    def _on_search(self, mot: str) -> None:
        rows = self.service.rechercher(mot)
        display = [
            (r['id'], r['nom'], r['categorie'], r['prix'], r['stock'], r['seuil_alerte'])
            for r in rows
        ]
        self.table.populate(display)

    def _ajouter(self) -> None:
        ProduitForm(self, self.service, on_save=self.refresh)

    def _modifier(self) -> None:
        selection = self.table.focus()
        if not selection:
            messagebox.showinfo('Info', 'Selectionnez une ligne.')
            return
        values = self.table.item(selection)['values']
        produit_id = int(values[0])
        ProduitForm(self, self.service, produit_id, on_save=self.refresh)

    def _supprimer(self) -> None:
        selection = self.table.focus()
        if not selection:
            return
        produit_id = int(self.table.item(selection)['values'][0])
        if messagebox.askyesno('Confirmation', 'Supprimer ce produit ?'):
            self.service.supprimer(produit_id)
            self.refresh()


class ProduitForm(tk.Toplevel):
    def __init__(self, master: tk.Misc, service: ProduitService, produit_id=None, on_save=None):
        super().__init__(master)
        self.service = service
        self.produit_id = produit_id
        self.on_save = on_save
        self.title('Produit')
        labels = ['Nom', 'Categorie', 'Taille', 'Couleur', 'Prix', 'Stock', 'Seuil alerte']
        self.entries = []
        for i, lbl in enumerate(labels):
            tk.Label(self, text=lbl).grid(row=i, column=0, sticky='w', padx=5, pady=4)
            ent = tk.Entry(self)
            ent.grid(row=i, column=1, padx=5, pady=4)
            self.entries.append(ent)
        tk.Button(self, text='Enregistrer', command=self.save).grid(
            row=len(labels), column=0, columnspan=2, pady=8
        )
        if produit_id:
            prod = self.service.repo.get(produit_id)
            data = [
                prod['nom'],
                prod['categorie'],
                prod['taille'],
                prod['couleur'],
                prod['prix'],
                prod['stock'],
                prod['seuil_alerte'],
            ]
            for ent, val in zip(self.entries, data):
                ent.insert(0, val)

    def save(self) -> None:
        try:
            produit = Produit(
                id=self.produit_id,
                nom=self.entries[0].get(),
                categorie=self.entries[1].get(),
                taille=self.entries[2].get(),
                couleur=self.entries[3].get(),
                prix=float(self.entries[4].get()),
                stock=int(self.entries[5].get()),
                seuil_alerte=int(self.entries[6].get()),
            )
        except ValueError:
            messagebox.showerror('Erreur', 'Champs numeriques invalides.')
            return
        if self.produit_id:
            self.service.modifier(produit)
        else:
            self.service.ajouter(produit)
        if self.on_save:
            self.on_save()
        self.destroy()
