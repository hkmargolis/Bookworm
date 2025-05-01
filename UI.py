import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
import csv
from PIL import ImageTk, Image

CSV_FILE = "BookwormCatalog.csv"
DB_FILE = "BookwormCatalog.db"

class UI_class:

    def __init__(self):
        self.window = tk.Tk();
        self.new_entry_input = dict()

    def setup(self):
        self.window.geometry("500x400")
        self.window.title("Bookworm")
        self.window.configure(bg="grey")
        display_main_menu(self.window)

def display_main_menu(window):
    for widget in window.winfo_children():
        widget.destroy()
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

    # add search label
    # search_label = tk.Label(window, text="Search")
    # search_label.grid(row=2, column=0, pady=5)
    # search_field = tk.Entry(window, width=30)
    # search_field.grid(row=2, column=1, pady=5)

    #add new entry button
    new_entry_button = tk.Button(window, text="Add entry",command=lambda: add_entry(window))
    new_entry_button.grid(row=3, column=0, pady=5)

    #add view label
    new_entry_button = tk.Button(window, text="View Catalog", command=lambda: view_catalog(window))
    new_entry_button.grid(row=3, column=1, pady=5)

def view_catalog(window):
    df = get_catalog()

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


def display_entry_ui(window):
    title_label = tk.Label(window, text="Title", anchor="center")
    title_label.grid(row=0, column=0,pady=1)
    title_entry = tk.Entry(window, width=30, justify="center")
    title_entry.grid(row=0, column=1,pady=1)

    author_label = tk.Label(window, text="Author", anchor="center")
    author_label.grid(row=1, column=0,pady=1)
    author_entry = tk.Entry(window, width=30, justify="center")
    author_entry.grid(row=1, column=1,pady=1)

    pub_year_label = tk.Label(window, text="PubYear", anchor="center")
    pub_year_label.grid(row=2, column=0,pady=1)
    pub_year_entry = tk.Entry(window, width=30, justify="center")
    pub_year_entry.grid(row=2, column=1,pady=1)

    genre_label = tk.Label(window, text="Genre", anchor="center")
    genre_label.grid(row=3, column=0,pady=1)
    genre_entry = tk.Entry(window, width=30, justify="center")
    genre_entry.grid(row=3, column=1,pady=1)

    rating_label = tk.Label(window, text="Rating", anchor="center")
    rating_label.grid(row=4, column=0,pady=1)
    rating_scale = tk.Scale(window, from_=1, to=5, orient='horizontal')
    rating_scale.grid(row=4, column=1,pady=1)

    note_label = tk.Label(window, text="Note", anchor="center")
    note_label.grid(row=5, column=0,pady=1)
    note_entry = tk.Text(window, height=5, width=30)
    note_entry.grid(row=5, column=1,pady=1)

    # add main menu button
    mm_button = tk.Button(window, text="Main Menu", command=lambda: display_main_menu(window))
    mm_button.grid(row=6, column=2, pady=5)

    return [title_entry, author_entry, pub_year_entry, genre_entry, rating_scale, note_entry]

def get_new_entry_input(window, input_fields):
    print("---get new entry input---")
    keys = ['note', 'rating', 'genre', 'pubYear', 'author', 'title']
    values = []
    #print(input_fields)

    for field in input_fields:
        if(type(field) is tk.Text):
            values.append(field.get("1.0",END))
        else:
            values.append(field.get())

    new_entry_input = dict(zip(keys, values))


def add_entry(window):
    print("---add entry---")
    for widget in window.winfo_children():
        widget.destroy()
    input_fields = display_entry_ui(window)

    new_entry_button = tk.Button(window, text="Add entry", command=lambda: get_new_entry_input(window, input_fields))
    new_entry_button.grid(row=6, column=1, pady=5)

    # save to db
    # add_new_entry_to_db()
    # print(new_entry_input)

def get_catalog():
    print("---get catalog---")
    conn = None
    df= None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        query = "SELECT * FROM Catalog"
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        df = pd.DataFrame(result, columns=column_names)

    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        conn.rollback()
    finally:
        conn.close()
    return df

def add_new_entry_to_db():
    print("---add new entry---")
    pass

def edit_db_entry():
    print("---edit entry---")
    pass

def csv_to_db():
    print("---csv_to_db---")
    conn = None
    try:
        #find or create db and connect
        conn = sqlite3.connect(DB_FILE)

        #create table if it doesn't exist
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Catalog (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Author TEXT,
                PubYear INTEGER,
                Genre TEXT,
                Rating INTEGER,
                Notes TEXT
            )
            '''
        )
        conn.commit()

        #get panda dataframe from csv
        df = pd.read_csv(CSV_FILE, delimiter="|")

        #insert dataframe into db
        df.to_sql("Catalog", conn, if_exists='replace', index=False)
        conn.commit()

    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        conn.rollback()
    finally:
        conn.close()

def db_to_csv() -> None:
    print("db_to_csv")
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        query = "SELECT * FROM Catalog"
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        df = pd.DataFrame(result, columns=column_names)
        df.to_csv(CSV_FILE, sep="|")
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        conn.rollback()
    finally:
        conn.close()

def main() -> None:
    csv_to_db()
    ui = UI_class()
    ui.setup()
    tk.mainloop()

# Run main automatically if this file is run directly - DO NOT EDIT
if __name__ == '__main__':
    main()