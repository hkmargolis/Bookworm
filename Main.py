import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
import csv
from PIL import ImageTk, Image
import UI
import Queries

def main() -> None:
    Queries.csv_to_db()
    ui = UI.UI_class()
    ui.setup()
    tk.mainloop()

# Run main automatically if this file is run directly - DO NOT EDIT
if __name__ == '__main__':
    main()