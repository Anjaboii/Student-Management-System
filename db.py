import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

# Debug: Print environment variables
print("🔍 Environment Variables:")
print(f"MYSQLHOST: {os.environ.get('MYSQLHOST')}")
print(f"MYSQLPORT: {os.environ.get('MYSQLPORT')}")
print(f"MYSQLDATABASE: {os.environ.get('MYSQLDATABASE')}")
print(f"MYSQLUSER: {os.environ.get('MYSQLUSER')}")
print(f"MYSQLPASSWORD: {os.environ.get('MYSQLPASSWORD')}")

# Railway DB config using environment variables
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

# Get database connection
def get_connection():
    try:
        print("🔗 Attempting database connection...")
        print(f"Host: {DB_CONFIG['host']}")
        print(f"Database: {DB_CONFIG['database']}")
        print(f"User: {DB_CONFIG['user']}")
        
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database")
            return connection
        raise Exception("Failed to connect to database")
    except Error as e:
        print(f"❌ Database connection error: {e}")
        raise Exception(f"Database connection error: {e}")

# Create the students table if not exists
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

# Run this only when directly executed
def init_database():
    create_students_table()

if __name__ == "__main__":
    init_database()