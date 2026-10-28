import tkinter as tk
from tkinter import tkk, messagebox
import sqlite3

DB_NAME = "prediksi_diabetes.db"

# fungsi untuk menjalankan query SQL
def run_query(sql, params=()):
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            return conn.execute(sql, params).fetchall()
    finally:
        conn.close()