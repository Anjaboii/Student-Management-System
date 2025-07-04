import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # leave blank if no password for XAMPP
        database='students'  # Make sure this DB is created in phpMyAdmin
    )
