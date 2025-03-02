import platform
import tkinter as tk
from tkinter import ttk

from .views import SearchPage
from .models import LocalDatabase


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = LocalDatabase()
        self.settings = None

        # Title and icon of the windows
        self.title("Popcitycle Search Engine")
        if platform.system()=="Linux":
            self.iconbitmap("@./app/images/logo.xbm")
        elif platform.system()=="Windows":
            self.iconbitmap("./app/images/logo.ico")

        # Display first frame
        self.search_page = SearchPage(self, self.model, self.settings)
        self.search_page.pack(expand=True, fill=tk.BOTH)
