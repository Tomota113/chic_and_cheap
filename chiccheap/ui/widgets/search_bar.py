import tkinter as tk
from typing import Callable


class SearchBar(tk.Frame):
    def __init__(self, master: tk.Misc, on_search: Callable[[str], None], **kwargs):
        super().__init__(master, **kwargs)
        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        btn = tk.Button(self, text='Rechercher', command=self._submit)
        btn.pack(side=tk.LEFT, padx=4)
        self.on_search = on_search

    def _submit(self) -> None:
        self.on_search(self.entry.get().strip())
