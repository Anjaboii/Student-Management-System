import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Leave blank if no password for XAMPP
    'database': 'students',
    'autocommit': False,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def get_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
        else:
            raise Exception("Failed to connect to database")
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        raise Exception(f"Database connection error: {e}")

def test_connection():
    """Test the database connection"""
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
            print(f"✅ Successfully connected to MySQL Server")
            print(f"   Version: {version[0]}")
            print(f"   Database: {DB_CONFIG['database']}")
            cursor.close()
            connection.close()
            return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def create_students_table():
    """Create the students table if it doesn't exist"""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Create table with proper constraints
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL CHECK (age > 0 AND age < 150),
            grade VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ Students table created successfully or already exists")
        
        # Create indexes for better performance
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_name ON students (name);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_grade ON students (grade);")
            connection.commit()
            print("✅ Database indexes created successfully")
        except Error as e:
            print(f"Warning: Could not create indexes: {e}")
        
    except Error as e:
        print(f"❌ Error creating students table: {e}")
        if connection:
            connection.rollback()
        raise Exception(f"Database table creation error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def check_table_exists():
    """Check if students table exists"""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("SHOW TABLES LIKE 'students'")
        result = cursor.fetchone()
        
        if result:
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            print(f"✅ Students table exists with {count} records")
            return True
        else:
            print("ℹ️  Students table does not exist")
            return False
            
    except Error as e:
        print(f"❌ Error checking table: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_database_info():
    """Get database information"""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get table info
        cursor.execute("SHOW TABLE STATUS LIKE 'students'")
        table_info = cursor.fetchone()
        
        # Get record count
        cursor.execute("SELECT COUNT(*) as total_students FROM students")
        count_info = cursor.fetchone()
        
        return {
            'table_exists': table_info is not None,
            'total_students': count_info['total_students'] if count_info else 0,
            'table_engine': table_info['Engine'] if table_info else None,
            'table_collation': table_info['Collation'] if table_info else None
        }
        
    except Error as e:
        print(f"❌ Error getting database info: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def init_database():
    """Initialize the database with table"""
    print("🔄 Initializing database...")
    
    # Test connection
    if not test_connection():
        print("❌ Cannot proceed without database connection")
        return False
    
    try:
        # Create table
        create_students_table()
        
        # Check if table exists
        check_table_exists()
        
        # Show database info
        info = get_database_info()
        if info:
            print(f"📊 Database Status:")
            print(f"   Table exists: {info['table_exists']}")
            print(f"   Total students: {info['total_students']}")
            print(f"   Engine: {info['table_engine']}")
        
        print("✅ Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

# Initialize database when module is imported (optional)
if __name__ == "__main__":
    init_database()