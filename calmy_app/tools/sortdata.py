import sqlite3

DATABASE_PATH = "data/data.db"

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE new2 AS
SELECT *
FROM new
ORDER BY nama ASC;
""")

cursor.execute("DROP TABLE new;")

cursor.execute("ALTER TABLE new2 RENAME TO makanan;")

conn.commit()
conn.close()

print("Data berhasil diurutkan dan diperbarui di database.")

