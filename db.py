import os
import urllib.parse
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error, pooling

# Load environment variables
load_dotenv()

# Connection pool configuration
pool_config = {
    'pool_name': 'student_pool',
    'pool_size': 10,
    'pool_reset_session': True,
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': False,
    'time_zone': '+00:00'
}

# Database configuration
def get_db_config():
    """Get database configuration from environment variables"""
    
    # Try to use DATABASE_URL first (Railway's preferred method)
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Parse DATABASE_URL
        parsed = urllib.parse.urlparse(database_url)
        return {
            'host': parsed.hostname,
            'port': parsed.port or 3306,
            'database': parsed.path.lstrip('/'),
            'user': parsed.username,
            'password': parsed.password,
            **pool_config
        }
    
    # Fallback to individual environment variables
    return {
        'host': os.environ.get('MYSQLHOST', 'localhost'),
        'port': int(os.environ.get('MYSQLPORT', 3306)),
        'database': os.environ.get('MYSQLDATABASE', 'railway'),
        'user': os.environ.get('MYSQLUSER', 'root'),
        'password': os.environ.get('MYSQLPASSWORD', ''),
        **pool_config
    }

# Initialize connection pool
connection_pool = None

def init_connection_pool():
    """Initialize MySQL connection pool"""
    global connection_pool
    try:
        config = get_db_config()
        print(f"🔗 Initializing connection pool to {config['host']}:{config['port']}")
        connection_pool = pooling.MySQLConnectionPool(**config)
        print("✅ Connection pool initialized successfully")
        return True
    except Error as e:
        print(f"❌ Failed to initialize connection pool: {e}")
        return False

def get_connection():
    """Get database connection from pool"""
    global connection_pool
    
    # Initialize pool if not exists
    if connection_pool is None:
        if not init_connection_pool():
            raise Exception("Failed to initialize database connection pool")
    
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            return connection
        else:
            raise Exception("Failed to get active connection from pool")
    except Error as e:
        print(f"❌ Database connection error: {e}")
        raise Exception(f"Database connection error: {e}")

def execute_query(query, params=None, fetch=False):
    """Execute a query with proper connection handling"""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            if fetch == 'one':
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.rowcount
            
    except Error as e:
        if connection:
            connection.rollback()
        print(f"❌ Query execution error: {e}")
        raise Exception(f"Database query error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def create_tables():
    """Create necessary tables"""
    try:
        # Students table
        students_table = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL CHECK (age > 0 AND age < 150),
            grade VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_name (name),
            INDEX idx_grade (grade)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        execute_query(students_table)
        print("✅ Students table created successfully")
        
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        raise

def test_connection():
    """Test database connection"""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            print("✅ Database connection test successful")
            return True
        else:
            print("❌ Database connection test failed")
            return False
    except Exception as e:
        print(f"❌ Database connection test error: {e}")
        return False

# Initialize database on import
def init_database():
    """Initialize database with tables"""
    try:
        print("🔄 Initializing database...")
        if test_connection():
            create_tables()
            print("✅ Database initialized successfully")
        else:
            print("❌ Database initialization failed - connection test failed")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Run initialization when module is imported
if __name__ == "__main__":
    init_database()
else:
    # Initialize pool when imported
    init_connection_pool()