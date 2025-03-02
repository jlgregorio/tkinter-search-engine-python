import tkinter as tk
from tkinter import ttk


class SearchBar(ttk.Entry):
    """Entry with suggestions in a Listbox"""

    def __init__(self, master, fun=None, *arg, **kwargs):
        
        super().__init__(master, *arg, **kwargs)

        self.suggestion_fun = fun # compute suggestions for a given input
        self.suggestion_list = None
        self.bind("<KeyRelease>", self.create_suggestion_list)

    def create_suggestion_list(self, event):
        """Create a listbox containing suggestions based on the user's input"""

        # Remove previous suggestion list
        if self.suggestion_list is not None:
            self.suggestion_list.destroy()

        # Look for database entries starting with user's input text
        results = self.suggestion_fun(self.get())

        if len(results): # Only create Listbox if suggestions are available
            self.suggestion_list = tk.Listbox(
                self.master,
                font=self.cget("font"), # same font as Entry widget
                width=self.cget("width"), # same width as Entry widget
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

            # Select suggestion
            self.suggestion_list.bind("<<ListboxSelect>>", self.select_suggestion)

    def delete_suggestion_list(self, event):

        self.suggestion_list.destroy()

    def select_suggestion(self, event):
        """Replace text in Entry by suggestion selected in Listbox"""
        
        self.delete(0, tk.END)
        selected_item = self.suggestion_list.curselection()
        self.insert(0, self.suggestion_list.get(selected_item))
        
