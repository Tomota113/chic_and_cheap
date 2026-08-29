import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from chiccheap.db import get_connection
from chiccheap.services.rapport_service import RapportService


class RapportsView(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.conn = get_connection()
        self.service = RapportService(self.conn)

        filtres = tk.Frame(self)
        filtres.pack(fill=tk.X, pady=5)
        tk.Label(filtres, text='Debut (YYYY-MM-DD)').pack(side=tk.LEFT, padx=5)
        tk.Label(filtres, text='Fin').pack(side=tk.LEFT, padx=5)
        debut, fin = self.service.periode_default()
        self.debut_var = tk.StringVar(value=debut.split()[0])
        self.fin_var = tk.StringVar(value=fin.split()[0])
        tk.Entry(filtres, textvariable=self.debut_var, width=12).pack(side=tk.LEFT, padx=5)
        tk.Entry(filtres, textvariable=self.fin_var, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(filtres, text='Charger', command=self.refresh).pack(side=tk.LEFT, padx=8)
        tk.Button(filtres, text='Export CSV', command=self.export_csv).pack(side=tk.LEFT, padx=8)

        self.table = ttk.Treeview(
            self,
            columns=('id', 'date', 'client', 'total_ht', 'taxe', 'remise', 'total_ttc'),
            show='headings',
        )
        for col in self.table['columns']:
            self.table.heading(col, text=col.upper())
        self.table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.top_label = tk.Label(self, text='Top produits :')
        self.top_label.pack(anchor='w', padx=5, pady=4)

        self.refresh()

    def refresh(self) -> None:
        debut = f"{self.debut_var.get()} 00:00:00"
        fin = f"{self.fin_var.get()} 23:59:59"
        self.table.delete(*self.table.get_children())
        rows = self.service.ventes_par_jour(debut, fin)
        for r in rows:
            self.table.insert('', tk.END, values=(r['id'], r['date'], r['client_id'], r['total_ht'], r['taxe'], r['remise_pct'], r['total_ttc']))
        top = self.service.top_produits()
        txt = 'Top produits : ' + ', '.join([f"{t['produit_id']} ({t['total_qte']})" for t in top])
        self.top_label.config(text=txt)

    def export_csv(self) -> None:
        debut = f"{self.debut_var.get()} 00:00:00"
        fin = f"{self.fin_var.get()} 23:59:59"
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV', '*.csv')])
        if not path:
            return
        try:
            self.service.export_ventes_csv(debut, fin, path)
            messagebox.showinfo('OK', 'Export realise.')
        except Exception as exc:
            messagebox.showerror('Erreur', str(exc))
