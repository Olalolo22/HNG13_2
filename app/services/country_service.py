import requests
import random
from datetime import datetime
from app.config import Config
from app.models import Country
from app.services.exchange_service import ExchangeService
from app.services.image_service import ImageService

class CountryService:
    """Service for country data operations"""
    
    @staticmethod
    def fetch_and_refresh():
        """Fetch countries and exchange rates, then cache in database"""
        try:
            # Fetch countries data
            countries_response = requests.get(
                Config.COUNTRIES_API_URL,
                timeout=Config.API_TIMEOUT
            )
            countries_response.raise_for_status()
            countries_data = countries_response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Could not fetch data from REST Countries API: {str(e)}")
        
        try:
            # Fetch exchange rates
            exchange_rates = ExchangeService.fetch_exchange_rates()
            
        except Exception as e:
            raise Exception(f"Could not fetch data from Exchange Rate API: {str(e)}")
        
        # Process countries data
        processed_countries = []
        current_time = datetime.now()
        
        for country in countries_data:
            name = country.get('name')
            capital = country.get('capital')
            region = country.get('region')
            population = country.get('population')
            flag_url = country.get('flag')
            currencies = country.get('currencies', [])
            
            # Validation: name and population are required
            if not name or population is None:
                continue
            
            # Currency handling
            currency_code = None
            exchange_rate = None
            estimated_gdp = 0
            
            if currencies and len(currencies) > 0:
                # Get first currency code
                currency_code = currencies[0].get('code')
                
                if currency_code:
                    # Get exchange rate
                    exchange_rate = exchange_rates.get(currency_code)
                    
                    if exchange_rate:
                        # Calculate estimated GDP
                        random_multiplier = random.uniform(1000, 2000)
                        estimated_gdp = (population * random_multiplier) / exchange_rate
                    else:
                        # Currency not found in exchange rates
                        exchange_rate = None
                        estimated_gdp = None
            
            processed_countries.append((
                name,
                capital,
                region,
                population,
                currency_code,
                exchange_rate,
                estimated_gdp,
                flag_url,
                current_time
            ))
        
        # Batch upsert to database
        if processed_countries:
            Country.upsert_batch(processed_countries)
            Country.update_refresh_timestamp()
        
        # Generate summary image
        try:
            ImageService.generate_summary_image()
        except Exception as e:
            print(f"Error generating image: {e}")
            # Don't fail the entire refresh if image generation fails
        
        return len(processed_countries)
    
    @staticmethod
    def get_countries(region=None, currency=None, sort=None):
        """Get countries with filters and sorting"""
        return Country.get_all(region=region, currency=currency, sort=sort)
    
    @staticmethod
    def get_country_by_name(name):
        """Get single country by name"""
        country = Country.get_by_name(name)
        if not country:
            return None
        return country
    
    @staticmethod
    def delete_country(name):
        """Delete country by name"""
        return Country.delete_by_name(name)
    
    @staticmethod
    def get_status():
        """Get API status"""
        total = Country.count()
        last_refresh = Country.get_last_refresh()
        
        return {
            "total_countries": total,
            "last_refreshed_at": last_refresh.isoformat() + 'Z' if last_refresh else None
        }