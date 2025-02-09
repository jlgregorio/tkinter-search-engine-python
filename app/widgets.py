import tkinter as tk
from tkinter import ttk


class SearchBar(ttk.Entry):
    """Entry with autocompletion and suggestions"""

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

    # TODO: add autocompletion and suggestions
    def create_suggestion_list(self, event):

        pass
        #self.suggestion_list = tk.Listbox(self.master, width=)
        # Place at bottom left corner of the Entry
        #self.suggestion_list.place(x=, y=)

    def delete_suggestion_list(self, event):

        self.suggestion_list.destroy()

    def update_suggestion_list(self, event):

        pass
        
