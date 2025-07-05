import os
import urllib.parse
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error, pooling

load_dotenv()

pool_config = {
    'pool_name': 'student_pool',
    'pool_size': 10,
    'pool_reset_session': True,
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': False,
    'time_zone': '+00:00'
}

def get_db_config():
    mysql_host = os.environ.get('MYSQL_HOST') or os.environ.get('MYSQLHOST')
    mysql_port = os.environ.get('MYSQL_PORT') or os.environ.get('MYSQLPORT')
    mysql_database = os.environ.get('MYSQL_DATABASE') or os.environ.get('MYSQLDATABASE')
    mysql_user = os.environ.get('MYSQL_USER') or os.environ.get('MYSQLUSER')
    mysql_password = os.environ.get('MYSQL_PASSWORD') or os.environ.get('MYSQLPASSWORD')

    if all([mysql_host, mysql_port, mysql_database, mysql_user, mysql_password]):
        print(f"🔗 Using MySQL variables: {mysql_host}:{mysql_port}")
        return {
            'host': mysql_host,
            'port': int(mysql_port),
            'database': mysql_database,
            'user': mysql_user,
            'password': mysql_password,
            **pool_config
        }

    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        parsed = urllib.parse.urlparse(database_url)
        print(f"🔗 Using DATABASE_URL: {parsed.hostname}:{parsed.port}")
        return {
            'host': parsed.hostname,
            'port': parsed.port or 3306,
            'database': parsed.path.lstrip('/'),
            'user': parsed.username,
            'password': parsed.password,
            **pool_config
        }

    host = mysql_host or 'localhost'
    port = int(mysql_port) if mysql_port else 3306
    database = mysql_database or 'students'
    user = mysql_user or 'root'
    password = mysql_password or ''

    print(f"🔗 Using fallback variables: {host}:{port} database: {database}")

    return {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password,
        **pool_config
    }

connection_pool = None

def init_connection_pool():
    global connection_pool
    if connection_pool:
        return True  # already initialized
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
    global connection_pool
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

# Initialize connection pool at import
init_connection_pool()
