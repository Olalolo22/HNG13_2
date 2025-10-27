import requests
from app.config import Config

class ExchangeService:
    """Service for fetching exchange rates"""
    
    @staticmethod
    def fetch_exchange_rates():
        """Fetch exchange rates from external API"""
        try:
            response = requests.get(
                Config.EXCHANGE_API_URL,
                timeout=Config.API_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract rates dictionary
            rates = data.get('rates', {})
            return rates
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Exchange rate API error: {str(e)}")