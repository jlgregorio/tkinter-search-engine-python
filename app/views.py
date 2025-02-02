import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from .widgets import SearchBar


class SearchPage(tk.Frame):
    """Interface looking like a web browser search engine page"""

    def __init__(self, parent, model, settings, *args, **kwargs):
        
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.model = model
        self.settings = settings

        self.parent.geometry("1280x720")
        
        img = Image.open("./app/images/search_page_logo.png")
        img = img.resize((270, 90))
        self.img = ImageTk.PhotoImage(img)
        self.panel = ttk.Label(self, image=self.img)
        self.panel.pack(side=tk.TOP, padx=10, pady=10)

        self.label = ttk.Label(self, text="Enter your search here")
        self.label.pack(side=tk.TOP, padx=10, pady=10)

        self.search_bar = SearchBar(self, font="Helvetica 20 bold")
        self.search_bar.bind("<Return>", self.search)
        self.search_bar.pack(fill=tk.X, padx=25, pady=10)

        self.results_area = ttk.Treeview(self)
        self.results_area['columns']=("city", "country", "year", "population")
        self.results_area.column("#0", width=0, stretch=tk.NO)
        self.results_area.column("city", anchor=tk.CENTER)
        self.results_area.column("country", anchor=tk.CENTER)
        self.results_area.column("year", anchor=tk.CENTER)
        self.results_area.column("population", anchor=tk.CENTER)
        self.results_area.heading("#0", text='', anchor=tk.CENTER)
        self.results_area.heading("city", text="City", anchor=tk.CENTER)
        self.results_area.heading("country", text="Country", anchor=tk.CENTER)
        self.results_area.heading("year", text="Year", anchor=tk.CENTER)
        self.results_area.heading("population", text="Annual population", anchor=tk.CENTER)
        self.results_area.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=10)

    def search(self, event):

        # Erase previous results
        self.results_area.delete(*self.results_area.get_children())

        # Get user's search (TODO: parse)
        raw_input = self.search_bar.get()

        # Query (TODO: add parameters and string matching)
        results = self.model.search(raw_input)

        # Show results
        for i, result in enumerate(results):
            self.results_area.insert(parent='', index="end", iid=i, text='', values=result)

