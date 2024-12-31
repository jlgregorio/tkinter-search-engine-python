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

        self.title("Custom Application")

        self.search_page = SearchPage(self, self.model, self.settings)

        self.search_page.pack(expand=True, fill=tk.BOTH)
