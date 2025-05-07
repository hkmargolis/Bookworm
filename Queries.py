import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
import csv
from PIL import ImageTk, Image

CSV_FILE = "BookwormCatalog.csv"
DB_FILE = "BookwormCatalog.db"

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
                Title TEXT,
                Author TEXT,
                PubYear TEXT,
                Genre TEXT,
                Rating INTEGER,
                Notes TEXT
            )
            '''
        )
        conn.commit()

        #get panda dataframe from csv
        df = pd.read_csv(CSV_FILE, delimiter="|", dtype={"PubYear":str})

        #insert dataframe into db
        df.to_sql("Catalog", conn, if_exists='replace', index=False)
        conn.commit()

    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        conn.rollback()
    finally:
        conn.close()

def db_to_csv():
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

def add_entry_to_db(values):
    print("---add new entry to db---")
    columns = 'Title','Author','PubYear','Genre','Rating','Note'

    query = f"INSERT OR REPLACE INTO Catalog {columns} VALUES ({values});"

    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        db_to_csv()
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        conn.rollback()
        return "Could not add item to database."
    finally:
        conn.close()

    return "Successfully added item to database."

def search_db(type_string, search_string):
    print("---search db---")
    query = f"SELECT * FROM Catalog WHERE {type_string} LIKE {search_string};"
    print(query)

    conn = None
    df = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
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

def delete_entry_from_db(type_string, search_string):
    print("---delete entry from db---")
    search_query = f"SELECT * FROM Catalog WHERE {type_string} LIKE {search_string};"
    delete_query = f"DELETE FROM Catalog WHERE {type_string} = {search_string};"

    conn = None
    df = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(search_query)

        row_count = len(cursor.fetchall())

        if row_count == 0:
            conn.close()
            return "Could not find item. View catalog and enter exact data value."

        elif row_count > 1:
            conn.close()
            return "Found more than one item that matches. View catalog and enter exact data value."

        else:
            cursor.execute(delete_query)

    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        conn.rollback()
        return "Could not delete item from database."
    finally:
        conn.close()
    return "Successfully deleted item from database."
