import tkinter as tk
from tkinter import messagebox

from chiccheap.config import DB_PATH, DEFAULT_DEVISE, DEFAULT_TAXE
from chiccheap.db import get_connection


class ParamsView(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.conn = get_connection()
        tk.Label(self, text=f'Base de donnees : {DB_PATH}').pack(anchor='w', padx=5, pady=4)

        tk.Label(self, text='Taux de taxe').pack(anchor='w', padx=5, pady=2)
        self.taxe_var = tk.StringVar(value=self._get_param('taxe', str(DEFAULT_TAXE)))
        tk.Entry(self, textvariable=self.taxe_var, width=10).pack(anchor='w', padx=5, pady=2)

        tk.Label(self, text='Devise').pack(anchor='w', padx=5, pady=2)
        self.devise_var = tk.StringVar(value=self._get_param('devise', DEFAULT_DEVISE))
        tk.Entry(self, textvariable=self.devise_var, width=10).pack(anchor='w', padx=5, pady=2)

        tk.Button(self, text='Enregistrer', command=self.save).pack(anchor='w', padx=5, pady=6)

    def _get_param(self, cle: str, default: str) -> str:
        row = self.conn.execute('SELECT valeur FROM parametre WHERE cle=?', (cle,)).fetchone()
        return row['valeur'] if row else default

    def save(self) -> None:
        for cle, val in (('taxe', self.taxe_var.get()), ('devise', self.devise_var.get())):
            self.conn.execute(
                'INSERT INTO parametre (cle, valeur) VALUES (?,?) ON CONFLICT(cle) DO UPDATE SET valeur=excluded.valeur',
                (cle, val),
            )
        self.conn.commit()
        messagebox.showinfo('OK', 'Parametres enregistres.')
