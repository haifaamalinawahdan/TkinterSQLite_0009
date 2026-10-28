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

# Validasi input
def read_form():
    nama = entries["nama"].get().strip()
    usia = entries["usia"].get().strip()
    gula = entries["gula"].get().strip()
    bmi = entries["bmi"].get().strip()
    riwayat = riwayat_var.get()

    if not nama or not usia or not gula or not bmi or not riwayat:
        messagebox.showwarning(
            "Data Kosong",
            "Semua data pasien harus diisi!"
        )
        return None

    try:
        usia = int(usia)
        gula = float(gula)
        bmi = float(bmi)
    except ValueError:
        messagebox.showwarning(
            "Input Tidak Valid",
            "Usia harus bilangan bulat, sedangkan gula darah "
            "dan BMI harus berupa angka."
        )
        return None

    if not 1 <= usia <= 120:
        messagebox.showwarning(
            "Usia Tidak Valid",
            "Usia harus antara 1 sampai 120 tahun."
        )
        return None

    if not 0 < gula <= 600:
        messagebox.showwarning(
            "Gula Darah Tidak Valid",
            "Gula darah harus lebih dari 0 dan maksimal 600 mg/dL."
        )
        return None

    if not 10 <= bmi <= 80:
        messagebox.showwarning(
            "BMI Tidak Valid",
            "BMI harus antara 10 sampai 80."
        )
        return None

    return nama, usia, gula, bmi, riwayat

# Menentukan prediksi risiko
def prediksi_diabetes(gula, bmi, riwayat):

    if gula >= 200:
        if riwayat == "Ya":
            return ("Risiko Sangat Tinggi (Indikasi Diabetes + Genetik)",
                  "#ff5555",
            )
        else:
            return (
                 "Risiko Tinggi (Indikasi Diabetes)", 
               "#ff5555"
            )

    elif 140 <= gula < 200:
        if bmi >= 30 or riwayat == "Ya":
            return (
                "Risiko Tinggi (Prediabetes + Genetik/Obesitas)",
                "#ffb86c"
            )           
        else:
            return (
                "Risiko Sedang (Prediabetes)",
              "#ffb86c"
            )
    else:
        if bmi >= 30:
            if riwayat == "Ya":
                return (
                "Risiko Sedang (Normal + Obesitas & Genetik)",
                "#f1fa8c",
            )
            else:
                return (
                    "Risiko Waspada (Normal + Obesitas)", 
                    "#f1fa8c"
                )
        elif riwayat == "Ya":
            return (
                "Risko Waspada (Gula Normal + Riwayat Genetik)",
                "#f1fa8c",
            )
        else:
            return (
                "Risiko Rendah (Normal)",
                  "#50fa7b"
            )

# Menampilkan hasil prediksi
var_hasil = tk.StringVar(value="-")

tk.Label(
    root,
    text="Hasil Prediksi Risiko Diabetes:",
    font=("Arial", 11, "bold")
).grid(row=1, column=0, pady=(5, 0))

label_hasil = tk.Label(
    root,
    textvariable=var_hasil,
    font=("Arial", 16, "bold"),
    fg="black",
    relief=tk.RAISED,
    width=22,
    pady=8
)
label_hasil.grid(row=2, column=0, padx=15, pady=8)