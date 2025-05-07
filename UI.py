import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
import csv
from PIL import ImageTk, Image
import Queries

CSV_FILE = "BookwormCatalog.csv"
DB_FILE = "BookwormCatalog.db"

class UI_class:

    def __init__(self):
        self.window = tk.Tk()
        self.new_entry_input = dict()

    def setup(self):
        self.window.geometry("1000x700")
        self.window.title("Bookworm")
        self.window.configure(bg="black")
        display_main_menu(self.window)

def display_exogorth():
    image = None
    photo = None
    try:
        image_path = "exogorth_books.png"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
    except FileNotFoundError:
        print("Error: Image not found. Please check the file path.")

    # add image
    image_label = tk.Label(image=photo)
    image_label.image = photo
    image_label.grid(row=0, column=0, columnspan=2)

def display_main_menu(window):
    for widget in window.winfo_children():
        widget.destroy()

    display_exogorth()

    # add search label
    search_label = tk.Label(window, text="Search")
    search_label.grid(row=2, column=0, pady=5)
    search_field = tk.Entry(window, width=30)
    search_field.grid(row=2, column=1, pady=5)

    # Dropdown options
    types = ["Title", "Author", "PubYear", "Genre", "Rating", "Note"]

    # Combobox
    cb = ttk.Combobox(window, values=types)
    cb.set("Search Type")
    cb.grid(row=2, column=3)

    search_button = tk.Button(window, text="Search",  command=lambda: search_catalog(window,cb,search_field))
    search_button.grid(row=2, column=4, pady=5)

    #add new entry button
    new_entry_button = tk.Button(window, text="Add entry",command=lambda: display_add_entry(window))
    new_entry_button.grid(row=3, column=0, pady=5)

    #add view label
    view_cat_button = tk.Button(window, text="View Catalog", command=lambda: view_catalog(window))
    view_cat_button.grid(row=4, column=0, pady=5)

def view_catalog(window):
    df = Queries.get_catalog()

    tree = ttk.Treeview(window, selectmode="browse")
    tree["columns"] = list(df.columns)
    for col in df.columns:
        tree.column(col, width=100)
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    tree.grid(row=5, columnspan=2)

    # Create vertical scrollbar
    vsb = ttk.Scrollbar(window, orient="vertical", command=tree.yview)

    # Create horizontal scrollbar
    hsb = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)

    # Configure Treeview to use scrollbars
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Place widgets using grid layout
    tree.grid(row=6, column=0, columnspan=2, sticky="nsew")
    vsb.grid(row=6, column=2, sticky="ns")
    hsb.grid(row=7, column=0, columnspan=2, sticky="ew")

def display_add_entry(window):
    print("---add entry---")
    # clear fields from previous window
    for widget in window.winfo_children():
        widget.destroy()

    display_exogorth()

    title_label = tk.Label(window, text="Title", anchor="center",fg="white", bg="black")
    title_label.grid(row=0, column=0,pady=1)
    title_entry = tk.Entry(window, width=30, justify="center")
    title_entry.grid(row=0, column=1,pady=1)

    author_label = tk.Label(window, text="Author", anchor="center",fg="white", bg="black")
    author_label.grid(row=1, column=0,pady=1)
    author_entry = tk.Entry(window, width=30, justify="center")
    author_entry.grid(row=1, column=1,pady=1)

    pub_year_label = tk.Label(window, text="PubYear", anchor="center",fg="white", bg="black")
    pub_year_label.grid(row=2, column=0,pady=1)
    pub_year_entry = tk.Entry(window, width=30, justify="center")
    pub_year_entry.grid(row=2, column=1,pady=1)

    genre_label = tk.Label(window, text="Genre", anchor="center",fg="white", bg="black")
    genre_label.grid(row=3, column=0,pady=1)
    genre_entry = tk.Entry(window, width=30, justify="center")
    genre_entry.grid(row=3, column=1,pady=1)

    rating_label = tk.Label(window, text="Rating", anchor="center",fg="white", bg="black")
    rating_label.grid(row=4, column=0,pady=1)
    rating_scale = tk.Scale(window, from_=1, to=5, orient='horizontal')
    rating_scale.grid(row=4, column=1,pady=1)

    note_label = tk.Label(window, text="Note", anchor="center",fg="white", bg="black")
    note_label.grid(row=5, column=0,pady=1)
    note_entry = tk.Text(window, height=5, width=30)
    note_entry.grid(row=5, column=1,pady=1)

    # add main menu button
    mm_button = tk.Button(window, text="Main Menu", command=lambda: display_main_menu(window))
    mm_button.grid(row=6, column=2, pady=5)

    input_fields = [title_entry, author_entry, pub_year_entry, genre_entry, rating_scale, note_entry]
    submit_button = tk.Button(window, text="Submit", command=lambda: get_input(window, input_fields))
    submit_button.grid(row=6, column=1, pady=5)

def get_input(window, input_fields):
    print("---get new entry input---")
    values = ""
    print("input fields: " + str(input_fields))

    # add input to list of values
    for field in input_fields[:-1]:
        values += "'" + str(field.get()) + "',"

    # get last element
    values += "'" + str(input_fields[-1].get("1.0", "end-1c")) + "'"

    print("New Entry Values: " + str(values))
    result = Queries.add_entry_to_db(values)

    result_label = tk.Label(window, text=result, anchor="center", fg="white", bg="black")
    result_label.grid(row=10, column=0, pady=1)

def search_catalog(window, type_field, search_field):
    search_string = "'%" + str(search_field.get()) + "%'"
    type_string = str(type_field.get())
    df = Queries.search_db(type_string, search_string)

    tree = ttk.Treeview(window, selectmode="browse")
    tree["columns"] = list(df.columns)
    for col in df.columns:
        tree.column(col, width=100)
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    tree.grid(row=5, columnspan=2)

    # Create vertical scrollbar
    vsb = ttk.Scrollbar(window, orient="vertical", command=tree.yview)

    # Create horizontal scrollbar
    hsb = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)

    # Configure Treeview to use scrollbars
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Place widgets using grid layout
    tree.grid(row=6, column=0, columnspan=2, sticky="nsew")
    vsb.grid(row=6, column=2, sticky="ns")
    hsb.grid(row=7, column=0, columnspan=2, sticky="ew")