import mysql.connector
from mysql.connector import pooling
from app.config import Config
from contextlib import contextmanager

class Database:
    """Database connection pool manager"""
    
    _pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Initialize connection pool"""
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name=Config.DB_CONFIG['pool_name'],
                    pool_size=Config.DB_CONFIG['pool_size'],
                    host=Config.DB_CONFIG['host'],
                    port=Config.DB_CONFIG['port'],
                    database=Config.DB_CONFIG['database'],
                    user=Config.DB_CONFIG['user'],
                    password=Config.DB_CONFIG['password'],
                    charset=Config.DB_CONFIG['charset'],
                    autocommit=Config.DB_CONFIG['autocommit']
                )
                print("Database connection pool initialized")
            except mysql.connector.Error as e:
                print(f"Error initializing database pool: {e}")
                raise
    
    @classmethod
    @contextmanager
    def get_connection(cls):
        """Context manager for database connections"""
        if cls._pool is None:
            cls.initialize_pool()
        
        connection = None
        try:
            connection = cls._pool.get_connection()
            yield connection
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    @classmethod
    @contextmanager
    def get_cursor(cls, dictionary=True):
        """Context manager for database cursor"""
        with cls.get_connection() as connection:
            cursor = connection.cursor(dictionary=dictionary)
            try:
                yield cursor
                connection.commit()
            except Exception as e:
                connection.rollback()
                raise
            finally:
                cursor.close()

# Initialize pool on module import
Database.initialize_pool()