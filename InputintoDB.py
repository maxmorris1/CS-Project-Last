import sqlite3
import hashlib

db_file = "database.db"
sql_file = "SQL Schema.sql"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
with open(sql_file, 'r') as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)

def db_action(action, credientials):
    if action == 'staff credentials':
        username, password = credientials()
        cursor.execute("SELECT 1, StaffPassword FROM StaffLogin WHERE StaffUsername = ?", (username,))
        result, password_check = cursor.fetchone()
        if result == 1:
            passHash = hashlib.sha256(password.encode('utf-8'))
            passHashDig = passHash.hexdigest()
            if passHashDig == password_check


conn.commit()
conn.close()
