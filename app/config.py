import os
from dotenv import load_dotenv

load_dotenv()

# Get the base directory (project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'database': os.getenv('DB_NAME', 'country_currency_db'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': 'utf8mb4',
        'autocommit': True,
        'pool_size': 10,
        'pool_name': 'country_pool'
    }
    
    # External APIs
    COUNTRIES_API_URL = os.getenv(
        'COUNTRIES_API_URL',
        'https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies'
    )
    EXCHANGE_API_URL = os.getenv(
        'EXCHANGE_API_URL',
        'https://open.er-api.com/v6/latest/USD'
    )
    
    # API Settings
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    
    # Image settings - use absolute path
    IMAGE_PATH = os.path.join(BASE_DIR, 'cache', 'summary.png')