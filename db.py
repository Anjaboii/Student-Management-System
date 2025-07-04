import os
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('MYSQLHOST'),
    'port': int(os.environ.get('MYSQLPORT', 3306)),
    'database': os.environ.get('MYSQLDATABASE'),
    'user': os.environ.get('MYSQLUSER'),
    'password': os.environ.get('MYSQLPASSWORD'),
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': True
}

def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
        raise Exception("Failed to connect to database")
    except Error as e:
        raise Exception(f"Database connection error: {e}")
        
def create_students_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                grade VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Students table created or already exists")
    except Exception as e:
        print(f"❌ Failed to create students table: {e}")

def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()[0]
        print(f"✅ Connected to MySQL Server, Version: {version}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

def init_database():
    test_connection()
    create_students_table()

if __name__ == "__main__":
    init_database()
