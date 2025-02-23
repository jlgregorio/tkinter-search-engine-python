import tkinter as tk
from tkinter import ttk


class SearchBar(ttk.Entry):
    """Entry with autocompletion and suggestions"""

    def __init__(self, master, fun=None):
        
        super().__init__(master, font="Sans 24 bold", width=50)

        self.autofill_fun = fun

        #TODO: self.bind("<KeyRelease>",)

    # TODO: add autocompletion and suggestions
    def create_suggestion_list(self, event):

        # Look for database entries starting with user's input text
        results = self.autofill_fun(self.get())

        # Listbox
        self.suggestion_list = tk.Listbox(
            self.master,
            font="Sans 24", # Hardcoded value
            width=50, # Hardcoded value
            height=len(results),
            foreground="grey"
        )
        #Place at bottom left corner of the Entry
        self.suggestion_list.place(
            x=self.winfo_x(),
            y=self.winfo_y()+self.winfo_height()
        )

        # Fill with results
        for i, s in enumerate(results):
            self.suggestion_list.insert(i+1, s[0])

    def delete_suggestion_list(self, event):

        self.suggestion_list.destroy()

    def update_suggestion_list(self, event):

        pass
        
