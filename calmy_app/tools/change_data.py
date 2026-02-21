import sqlite3

conn = sqlite3.connect("data/data.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE calories_data;")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_lengkap TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        tanggal_lahir TEXT,
        program TEXT,
        jenis_kelamin TEXT,
        usia INTEGER,
        tinggi_badan INTEGER,
        berat_badan INTEGER,
        level_aktivitas TEXT,
        bmi_value REAL DEFAULT 0,
        bmr_value REAL DEFAULT 0,
        target_calories REAL DEFAULT 0,
        daily_calories REAL DEFAULT 0,
        daily_data TEXT --
        )
    ''')
    
cursor.execute('''
    CREATE TABLE IF NOT EXISTS calories_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        nama_makanan TEXT NOT NULL,
        jumlah REAL NOT NULL,
        satuan TEXT NOT NULL,
        kalori REAL NOT NULL,
        kategori TEXT NOT NULL,
        tanggal DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (username) REFERENCES user_data(username)
        )
    ''')
    
conn.commit()
conn.close()

nama_lengkap = "Daffa"
username = "dapp17"
password = "12345678"
program = "Peningkatan Berat Badan"
jenis_kelamin = "L"
tanggal_lahir = "17/05/2006"
usia = "18"
tinggi_badan = "165"
berat_badan = "47"
level_aktivitas = "Sedikit Aktif"

conn = sqlite3.connect("data/data.db")
cursor = conn.cursor()

try:
    cursor.execute('''
        UPDATE user_data SET(
            nama_lengkap, username, password, tanggal_lahir, program, 
            jenis_kelamin, usia, tinggi_badan, berat_badan, level_aktivitas
        )
        = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) WHERE id = ?
    ''', (
        nama_lengkap, username, password, tanggal_lahir, program, 
        jenis_kelamin, usia, tinggi_badan, berat_badan, level_aktivitas, 1
    ))
    conn.commit()
    print("Data pengguna berhasil disimpan!")
except sqlite3.IntegrityError:
    print("Invalid data")
finally:
    conn.close()
