import tkinter as tk
from chiccheap.db import init_db
from chiccheap.ui.login_window import LoginWindow


def main() -> None:
    init_db()
    root = tk.Tk()
    root.withdraw()
    LoginWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
