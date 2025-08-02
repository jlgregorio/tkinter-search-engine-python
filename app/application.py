"""Application or controller, holds references to the views and models (see MVC pattern)."""

import platform
import tkinter as tk
from tkinter import ttk

from .views import SearchPage
from .models import LocalDatabase


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.settings = { # TODO: add settings file and tab
            "suggestion_list_length":5,
            "data_file":"./data/WUP2018-F22-Cities_Over_300K_Annual.xlsx"
        } 
        
        self.model = LocalDatabase()
        # Check if empty and populate with data if necessary
        if not self.model.tables:
            self.model.build_database(self.settings["data_file"])

        # Title and icon of the windows
        self.title("Popcitycle Search Engine")
        if platform.system()=="Linux":
            self.iconbitmap("@./app/images/logo.xbm")
        elif platform.system()=="Windows":
            self.iconbitmap("./app/images/logo.ico")

        # Display first frame
        self.search_page = SearchPage(self, self.model, self.settings)
        self.search_page.pack(expand=True, fill=tk.BOTH)
