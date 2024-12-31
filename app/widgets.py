import tkinter as tk
from tkinter import ttk


class SearchBar(ttk.Entry):
    """Entry with autocompletion and suggestions"""

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

    # TODO: add autocompletion and suggestions
        
