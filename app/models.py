from app.database import Database
from datetime import datetime

class Country:
    """Country data model"""
    
    @staticmethod
    def get_all(region=None, currency=None, sort=None):
        """Get all countries with optional filters and sorting"""
        query = "SELECT * FROM countries WHERE 1=1"
        params = []
        
        if region:
            query += " AND LOWER(region) = LOWER(%s)"
            params.append(region)
        
        if currency:
            query += " AND LOWER(currency_code) = LOWER(%s)"
            params.append(currency)
        
        # Sorting
        if sort:
            if sort == 'gdp_desc':
                query += " ORDER BY estimated_gdp DESC"
            elif sort == 'gdp_asc':
                query += " ORDER BY estimated_gdp ASC"
            elif sort == 'name_asc':
                query += " ORDER BY name ASC"
            elif sort == 'population_desc':
                query += " ORDER BY population DESC"
            else:
                query += " ORDER BY name ASC"
        else:
            query += " ORDER BY name ASC"
        
        with Database.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    @staticmethod
    def get_by_name(name):
        """Get country by name (case-insensitive)"""
        query = "SELECT * FROM countries WHERE LOWER(name) = LOWER(%s)"
        
        with Database.get_cursor() as cursor:
            cursor.execute(query, (name,))
            return cursor.fetchone()
    
    @staticmethod
    def delete_by_name(name):
        """Delete country by name (case-insensitive)"""
        query = "DELETE FROM countries WHERE LOWER(name) = LOWER(%s)"
        
        with Database.get_cursor() as cursor:
            cursor.execute(query, (name,))
            return cursor.rowcount > 0
    
    @staticmethod
    def upsert_batch(countries_data):
        """Insert or update multiple countries"""
        query = """
            INSERT INTO countries 
            (name, capital, region, population, currency_code, exchange_rate, estimated_gdp, flag_url, last_refreshed_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                capital = VALUES(capital),
                region = VALUES(region),
                population = VALUES(population),
                currency_code = VALUES(currency_code),
                exchange_rate = VALUES(exchange_rate),
                estimated_gdp = VALUES(estimated_gdp),
                flag_url = VALUES(flag_url),
                last_refreshed_at = VALUES(last_refreshed_at)
        """
        
        with Database.get_cursor() as cursor:
            cursor.executemany(query, countries_data)
            return cursor.rowcount
    
    @staticmethod
    def count():
        """Get total number of countries"""
        query = "SELECT COUNT(*) as count FROM countries"
        
        with Database.get_cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result['count'] if result else 0
    
    @staticmethod
    def get_top_by_gdp(limit=5):
        """Get top countries by estimated GDP"""
        query = """
            SELECT name, estimated_gdp 
            FROM countries 
            WHERE estimated_gdp IS NOT NULL 
            ORDER BY estimated_gdp DESC 
            LIMIT %s
        """
        
        with Database.get_cursor() as cursor:
            cursor.execute(query, (limit,))
            return cursor.fetchall()
    
    @staticmethod
    def get_last_refresh():
        """Get last refresh timestamp"""
        query = "SELECT last_refreshed_at FROM refresh_metadata WHERE id = 1"
        
        with Database.get_cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result['last_refreshed_at'] if result else None
    
    @staticmethod
    def update_refresh_timestamp():
        """Update global refresh timestamp"""
        query = "UPDATE refresh_metadata SET last_refreshed_at = %s WHERE id = 1"
        
        with Database.get_cursor() as cursor:
            cursor.execute(query, (datetime.now(),))