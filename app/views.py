import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from .widgets import SearchBar


class SearchPage(ttk.Frame):
    """Interface looking like a web browser search engine page"""

    def __init__(self, master, model, settings, *args, **kwargs):
        
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.model = model
        self.settings = settings

        # Initial size of window
        self.master.geometry("1280x720")

        # Style configuration
        style = ttk.Style()
        style.configure("TFrame", background="#d3f2f5")
        style.configure("TLabel", background="#d3f2f5", font="Sans")
        style.configure("Treeview.Heading", font="Sans", background="#87bfc8")
        style.configure("Treeview", font="Sans", background="white")
        style.map("Treeview", background=[('selected', '#fab5ac')])

        # Logo
        img = Image.open("./app/images/search_page_logo.png")
        self.img = ImageTk.PhotoImage(img)
        self.panel = ttk.Label(self, image=self.img)
        self.panel.pack(side=tk.TOP, padx=10, pady=10)

        self.label = ttk.Label(self, text="Welcome, enter your search below!")
        self.label.pack(side=tk.TOP, padx=10, pady=10)

        self.search_bar = SearchBar(self, self.model.search_autofill, font="Sans 24 bold", width=50)
        self.search_bar.bind("<Return>", self.search)
        self.search_bar.pack(pady=10)

        self.results_area = ttk.Treeview(self)
        self.results_area['columns']=("city", "country", "year", "population")
        self.results_area.column("#0", width=0, stretch=tk.NO)
        self.results_area.column("city", anchor=tk.CENTER)
        self.results_area.column("country", anchor=tk.CENTER)
        self.results_area.column("year", anchor=tk.CENTER)
        self.results_area.column("population", anchor=tk.CENTER)
        self.results_area.heading("#0", text='', anchor=tk.CENTER)
        self.results_area.heading("city", text="Urban agglomeration", anchor=tk.CENTER)
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

