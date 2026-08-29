import tkinter as tk
from tkinter import ttk
from typing import Iterable, List


class TableView(ttk.Treeview):
    def __init__(self, master: tk.Misc, columns: List[str], **kwargs):
        super().__init__(master, columns=columns, show='headings', **kwargs)
        for col in columns:
            self.heading(col, text=col.capitalize())
            self.column(col, width=120, anchor=tk.CENTER)

    def populate(self, rows: Iterable[Iterable]):
        self.delete(*self.get_children())
        for row in rows:
            self.insert('', tk.END, values=row)
