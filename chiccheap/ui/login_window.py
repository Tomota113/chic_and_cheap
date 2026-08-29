import tkinter as tk
from tkinter import messagebox

from chiccheap.db import get_connection
from chiccheap.services.auth_service import AuthService
from chiccheap.ui.main_window import MainWindow
from chiccheap.config import THEME_BG, THEME_ACCENT


class LoginWindow(tk.Toplevel):
    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.title('Connexion - Chic and Cheap')
        self.configure(bg=THEME_BG)
        self.resizable(False, False)

        tk.Label(self, text="Nom d'utilisateur", bg=THEME_BG).grid(row=0, column=0, pady=5, padx=10)
        tk.Label(self, text='Mot de passe', bg=THEME_BG).grid(row=1, column=0, pady=5, padx=10)
        self.username = tk.Entry(self)
        self.password = tk.Entry(self, show='*')
        self.username.grid(row=0, column=1, pady=5, padx=10)
        self.password.grid(row=1, column=1, pady=5, padx=10)
        btn = tk.Button(self, text='Se connecter', bg=THEME_ACCENT, command=self.login)
        btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

        self.auth = AuthService(get_connection())

    def login(self) -> None:
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        role = self.auth.authenticate(user, pwd)
        if role:
            self.destroy()
            MainWindow(self.master, username=user, role=role)
        else:
            messagebox.showerror('Erreur', 'Identifiants invalides.')
