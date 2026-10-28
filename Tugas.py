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

# Mengambil seluruh data pasien
def get_pasien():
    return run_query("""
        SELECT id, nama_pasien, usia, gula_darah,
               bmi, riwayat_ortu, hasil_prediksi
        FROM pasien
        ORDER BY id DESC
    """)

# Membuat window
create_db()

root = tk.Tk()
root.title("Aplikasi Prediksi Risiko Diabetes")
root.resizable(False, False)

# untuk input data pasien
frame_input = tk.LabelFrame(
    root,
    text=" Data Pasien ",
    padx=15,
    pady=10
)
frame_input.grid(row=0, column=0, padx=15, pady=10)

entries = {}

fields = [
    ("Nama Pasien", "nama"),
    ("Usia", "usia"),
    ("Gula Darah (mg/dL)", "gula"),
    ("BMI", "bmi")
]

for i, (label, key) in enumerate(fields):
    tk.Label(frame_input, text=label).grid(
        row=i, column=0, sticky="w", padx=5, pady=5
    )

    entries[key] = tk.Entry(frame_input, width=25)
    entries[key].grid(
        row=i, column=1, padx=5, pady=5
    )


tk.Label(
    frame_input,
    text="Riwayat Diabetes Orang Tua"
).grid(row=4, column=0, sticky="w", padx=5, pady=5)

riwayat_var = tk.StringVar()

combo_riwayat = ttk.Combobox(
    frame_input,
    textvariable=riwayat_var,
    values=("Ya", "Tidak"),
    state="readonly",
    width=22
)
combo_riwayat.grid(
    row=4, column=1, padx=5, pady=5
)