"""Custom widgets."""

import tkinter as tk
from tkinter import ttk


class SearchBar(ttk.Entry):
    """Entry with suggestions in a Listbox below, similar to a search bar"""

    def __init__(self, master, fun, *arg, **kwargs):
        
        super().__init__(master, *arg, **kwargs)

        # Stores Entry input (text) in a StringVar for easier manipulation
        self.user_input = tk.StringVar()
        self["textvariable"] = self.user_input
        self.user_input.trace('w', self.create_suggestion_list)
        # Function used to compute suggestions for a given input
        self.suggestion_fun = fun
        # Obviously start with no suggestion list
        self.suggestion_list = None
        # Key bindings
        self.bind("<FocusOut>", self.delete_suggestion_list)
        self.bind("<Down>", self.scroll_suggestions)
        self.bind("<Up>", self.scroll_suggestions)
        self.bind("<Right>", self.select_suggestion)

    def create_suggestion_list(self, *args):
        """Create a listbox containing suggestions based on the user's input"""
        
        # Remove previous suggestion list (if any)
        if self.suggestion_list is not None:
            self.suggestion_list.destroy()
        
        # Look for database entries starting with user's input text
        if len(self.user_input.get()):
            results = self.suggestion_fun(
                self.user_input.get(),
                self.master.master.settings["suggestion_list_length"]
            )
            if not len(results):
                return # only show if suggestions are available
        else:
            return # do not show suggestions is search bar is empty

        # Create suggestion list
        self.suggestion_list = tk.Listbox(
            self.master,
            font=self.cget("font"), # same font as Entry widget
            width=self.cget("width"), # same width as Entry widget
            height=len(results),
            foreground="grey",
            selectmode=tk.SINGLE # select only one item at a time
        )
        # Place at bottom left corner of the Entry
        self.suggestion_list.place(
            x=self.winfo_x(),
            y=self.winfo_y()+self.winfo_height()
        )

        # Fill with results
        for i, s in enumerate(results):
            self.suggestion_list.insert(i+1, s[0])

        # Bind click
        self.suggestion_list.bind("<<ListboxSelect>>", self.select_suggestion)

    def delete_suggestion_list(self, event):
        """Delete suggestion ListBox"""

        if self.suggestion_list is not None:
            self.suggestion_list.destroy()

    def select_suggestion(self, event):
        """Replace text in Entry by suggestion selected in Listbox"""
        
        # No selection if no suggestion list to display
        if self.suggestion_list is None:
            return
        
        selected = self.suggestion_list.get(self.suggestion_list.curselection())
        self.delete(0, tk.END)
        self.insert(0, selected)
        self.suggestion_list.destroy()

    def scroll_suggestions(self, event):
        """Scroll through items in suggestion Listbox"""

        # No scrolling if no suggestion list to display
        if self.suggestion_list is None:
            return

        # Scroll up until first, start with last item if no selection
        if event.keysym == 'Up':
            if not self.suggestion_list.curselection():
                self.suggestion_list.selection_set(self.suggestion_list.size()-1)
            else:
                if (n:=self.suggestion_list.curselection()[-1]):
                    self.suggestion_list.select_clear(n)
                    self.suggestion_list.selection_set(n-1)

        # Scroll down until last, start with first item if no selection
        elif event.keysym == 'Down':
            if not self.suggestion_list.curselection():
                self.suggestion_list.selection_set(0)
            else:
                if (n:=self.suggestion_list.curselection()[-1]) != (self.suggestion_list.size() - 1):
                    self.suggestion_list.select_clear(n)
                    self.suggestion_list.selection_set(n+1)

