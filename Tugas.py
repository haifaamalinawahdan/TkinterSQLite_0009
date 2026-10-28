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

# membuat tabel
def create_db():
    run_query("""CREATE TABLE IF NOT EXISTS pasien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_pasien TEXT NOT NULL,
        usia INTEGER NOT NULL,
        gula_darah REAL NOT NULL,
        bmi REAL NOT NULL,
        riwayat_ortu TEXT NOT NULL,
        hasil_prediksi TEXT NOT NULL
    )""")

# fungsi untuk menambahkan data pasien
def add_pasien(nama, usia, gula, bmi, riwayat, hasil):
    run_query("""
        INSERT INTO pasien
        (nama_pasien, usia, gula_darah, bmi,
         riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nama, usia, gula, bmi, riwayat, hasil))