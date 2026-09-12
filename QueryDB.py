import sqlite3
import hashlib

db_file = "database.db"
sql_file = "SQL Schema.sql"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
with open(sql_file, 'r') as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()

def db_action(action, info_array):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    if action == 'check staff credentials':
        username, password = info_array
        cursor.execute("SELECT 1, StaffPassHex FROM StaffLogin WHERE StaffUsername = ?", (username,))
        row = cursor.fetchone()
        if row is None:
            return "New"
        _, password_check = row
        passHash = hashlib.sha256(password.encode('utf-8'))
        passHashDig = passHash.hexdigest()
        if passHashDig == password_check:
            credientials_check = 'Correct'
        else:
            credientials_check = 'Incorrect'
        return credientials_check
    elif action == 'new staff credentials':
        new_credientials, firstName, lastName, staffPosition = info_array
        username, password = new_credientials
        passHash = hashlib.sha256(password.encode('utf-8'))
        passHashDig = passHash.hexdigest()
        new_staff_member = (firstName, lastName, staffPosition) 
        cursor.execute("INSERT INTO Staff (StaffFirstName, StaffLastName, StaffPosition) VALUES (?, ?, ?)", new_staff_member)
        staff_id = cursor.lastrowid
        new_staff_creds = (staff_id, username, passHashDig)
        cursor.execute("INSERT INTO StaffLogin (StaffID, StaffUsername, StaffPassHex) VALUES (?, ?, ?)", new_staff_creds)
    elif action == 'check customer credentials':
        username, password = info_array
        cursor.execute("SELECT 1, CustomerPassHex FROM CustomersLogin WHERE CustomerUsername = ?", (username,))
        row = cursor.fetchone()
        if row is None:
            return "New"
        _, password_check = row
        passHash = hashlib.sha256(password.encode('utf-8'))
        passHashDig = passHash.hexdigest()
        if passHashDig == password_check:
            credientials_check = 'Correct'
        else:
            credientials_check = 'Incorrect'
        return credientials_check
    elif action == 'new customer credentials':
        new_credientials, firstName, lastName, phone, email = info_array
        username, password = new_credientials
        passHash = hashlib.sha256(password.encode('utf-8'))
        passHashDig = passHash.hexdigest()
        new_customer = (firstName, lastName, phone, email) 
        cursor.execute("INSERT INTO Customers (CustomerFirstName, CustomerLastName, CustomerPhone, CustomerEmail) VALUES (?, ?, ?, ?)", new_customer)
        customer_id = cursor.lastrowid
        new_customer_creds = (customer_id, username, passHashDig)
        cursor.execute("INSERT INTO CustomersLogin (CustomerID, CustomerUsername, CustomerPassHex) VALUES (?, ?, ?)", new_customer_creds)
    conn.commit()
    conn.close()


