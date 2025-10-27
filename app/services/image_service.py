from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from app.models import Country
from app.config import Config
import os

class ImageService:
    """Service for generating summary images"""
    
    @staticmethod
    def generate_summary_image():
        """Generate summary image with country statistics"""
        
        # Get data
        total_countries = Country.count()
        top_countries = Country.get_top_by_gdp(5)
        last_refresh = Country.get_last_refresh()
        
        # Image dimensions and colors
        width = 800
        height = 600
        bg_color = (255, 255, 255)
        text_color = (0, 0, 0)
        title_color = (25, 118, 210)
        header_color = (25, 118, 210)
        
        # Create image
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # Try to use a nicer font, fallback to default
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        y_offset = 40
        
        # Title
        title = "Country Currency API Summary"
        draw.text((width // 2, y_offset), title, fill=title_color, font=title_font, anchor="mm")
        y_offset += 80
        
        # Total countries
        total_text = f"Total Countries: {total_countries}"
        draw.text((50, y_offset), total_text, fill=text_color, font=header_font)
        y_offset += 60
        
        # Top 5 countries by GDP
        top_title = "Top 5 Countries by Estimated GDP:"
        draw.text((50, y_offset), top_title, fill=header_color, font=header_font)
        y_offset += 40
        
        for idx, country in enumerate(top_countries, 1):
            country_name = country['name']
            gdp = country['estimated_gdp']
            gdp_formatted = f"${gdp:,.2f}" if gdp else "N/A"
            
            country_text = f"{idx}. {country_name}: {gdp_formatted}"
            draw.text((70, y_offset), country_text, fill=text_color, font=body_font)
            y_offset += 35
        
        y_offset += 30
        
        # Last refresh timestamp
        if last_refresh:
            refresh_text = f"Last Refreshed: {last_refresh.strftime('%Y-%m-%d %H:%M:%S UTC')}"
        else:
            refresh_text = "Last Refreshed: Never"
        
        draw.text((50, y_offset), refresh_text, fill=text_color, font=body_font)
        
        # Save image
        os.makedirs('cache', exist_ok=True)
        image.save(Config.IMAGE_PATH)
        
        return Config.IMAGE_PATH