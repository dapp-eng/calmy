import pandas as pd
import sqlite3

excel_file_path = r'C:\Users\win 10\OneDrive\Dokumen\.Pemrograman Dasar 24A\Project Pemdas\calmy_app\dataset.xlsx'
database_path = r'C:\Users\win 10\OneDrive\Dokumen\.Pemrograman Dasar 24A\Project Pemdas\calmy_app\data\data.db'

df = pd.read_excel(excel_file_path)

print("Kolom yang ada di file Excel:", df.columns)
print("Jumlah NaN di kolom Jumlah:", df['Jumlah'].isnull().sum())
print("Jumlah NaN di kolom Satuan:", df['Satuan'].isnull().sum())
print("Jumlah NaN di kolom Kalori:", df['Kalori'].isnull().sum())

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS makanan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    jumlah REAL NOT NULL,
    kalori REAL NOT NULL,
    satuan TEXT NOT NULL
)
''')

for index, row in df.iterrows():
    nama = row['Nama']
    jumlah = row['Jumlah']
    satuan = row['Satuan']
    kalori = row['Kalori']
    
    cursor.execute('''
    INSERT INTO makanan (nama, jumlah, kalori, satuan) 
    VALUES (?, ?, ?, ?)
    ''', (nama, jumlah, kalori, satuan))

conn.commit()
conn.close()

print("Data dari Excel berhasil dimasukkan ke database SQLite!")
