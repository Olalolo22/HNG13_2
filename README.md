Country Currency & Exchange API
A RESTful API that fetches country data and exchange rates from external APIs, caches them in MySQL, and provides CRUD operations with image generation capabilities.
Features

Fetch country data from REST Countries API
Fetch real-time exchange rates
Calculate estimated GDP for each country
MySQL database caching
Filter and sort countries by region, currency, and GDP
Generate visual summary images
Complete CRUD operations
Proper error handling and validation

Tech Stack

Python 3.10+
Flask - Web framework
MySQL - Database
Pillow (PIL) - Image generation
Requests - HTTP client
mysql-connector-python - MySQL driver

Prerequisites

Python 3.10 or higher
MySQL 8.0 or higher
pip (Python package manager)

Installation
1. Clone the Repository
bashgit clone <your-repo-url>
cd country-currency-api
2. Create Virtual Environment
bashpython3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bashpip install -r requirements.txt
4. Setup MySQL Database
bash# Login to MySQL
mysql -u root -p

# Run the schema file
source migrations/schema.sql

# Or manually execute:
CREATE DATABASE country_currency_db;
5. Configure Environment Variables
bashcp .env.example .env
Edit .env with your database credentials:
envFLASK_ENV=development
PORT=5000

DB_HOST=localhost
DB_PORT=3306
DB_NAME=country_currency_db
DB_USER=root
DB_PASSWORD=yourpassword

API_TIMEOUT=30
6. Run the Application
bashpython run.py
The API will be available at http://localhost:5000
API Endpoints
1. Refresh Countries Data
POST /countries/refresh
Fetches all countries and exchange rates, then caches them in the database.
Response:
json{
  "message": "Countries refreshed successfully",
  "count": 250
}
Errors:

503 - External API unavailable


2. Get All Countries
GET /countries
Returns all countries with optional filters and sorting.
Query Parameters:

region - Filter by region (e.g., ?region=Africa)
currency - Filter by currency code (e.g., ?currency=NGN)
sort - Sort results:

gdp_desc - Highest GDP first
gdp_asc - Lowest GDP first
name_asc - Alphabetical by name
population_desc - Highest population first



Examples:
bashGET /countries?region=Africa
GET /countries?currency=NGN
GET /countries?sort=gdp_desc
GET /countries?region=Africa&sort=population_desc
Response:
json[
  {
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-22T18:00:00Z"
  }
]

3. Get Single Country
GET /countries/:name
Get a single country by name (case-insensitive).
Example:
bashGET /countries/Nigeria
Response:
json{
  "id": 1,
  "name": "Nigeria",
  "capital": "Abuja",
  "region": "Africa",
  "population": 206139589,
  "currency_code": "NGN",
  "exchange_rate": 1600.23,
  "estimated_gdp": 25767448125.2,
  "flag_url": "https://flagcdn.com/ng.svg",
  "last_refreshed_at": "2025-10-22T18:00:00Z"
}
Errors:

404 - Country not found


4. Delete Country
DELETE /countries/:name
Delete a country by name (case-insensitive).
Example:
bashDELETE /countries/Nigeria
Response:
json{
  "message": "Country 'Nigeria' deleted successfully"
}
Errors:

404 - Country not found


5. Get Status
GET /status
Returns total countries and last refresh timestamp.
Response:
json{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-22T18:00:00Z"
}

6. Get Summary Image
GET /countries/image
Serves the generated summary image containing:

Total number of countries
Top 5 countries by estimated GDP
Last refresh timestamp

Response:

Content-Type: image/png
Binary image data

Errors:

404 - Summary image not found


Project Structure
country-currency-api/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration
│   ├── database.py              # Database connection pool
│   ├── models.py                # Country data model
│   ├── routes.py                # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── country_service.py   # Country business logic
│   │   ├── exchange_service.py  # Exchange rate fetching
│   │   └── image_service.py     # Image generation
│   └── utils/
│       ├── __init__.py
│       └── validators.py        # Input validation
├── cache/
│   └── summary.png              # Generated summary image
├── migrations/
│   └── schema.sql               # Database schema
├── .env.example                 # Environment template
├── .gitignore
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md
Data Flow

Refresh Process:

Fetch countries from REST Countries API
Fetch exchange rates from Exchange Rate API
Extract first currency code for each country
Calculate estimated_gdp = population × random(1000-2000) ÷ exchange_rate
Upsert countries to database (update if exists, insert if new)
Generate summary image
Update global refresh timestamp


Currency Handling:

If country has multiple currencies, only the first is stored
If currencies array is empty:

currency_code = NULL
exchange_rate = NULL
estimated_gdp = 0


If currency not found in exchange rates:

exchange_rate = NULL
estimated_gdp = NULL




Update vs Insert:

Countries matched by name (case-insensitive)
Existing countries are updated with fresh data
New random multiplier generated on each refresh



Error Handling
The API returns consistent JSON error responses:
json// 404 Not Found
{
  "error": "Country not found"
}

// 400 Bad Request
{
  "error": "Validation failed",
  "details": {
    "currency_code": "is required"
  }
}

// 500 Internal Server Error
{
  "error": "Internal server error"
}

// 503 Service Unavailable
{
  "error": "External data source unavailable",
  "details": "Could not fetch data from REST Countries API"
}
Testing the API
Using cURL
bash# Refresh countries
curl -X POST http://localhost:5000/countries/refresh

# Get all countries
curl http://localhost:5000/countries

# Filter by region
curl http://localhost:5000/countries?region=Africa

# Filter by currency
curl http://localhost:5000/countries?currency=NGN

# Sort by GDP
curl http://localhost:5000/countries?sort=gdp_desc

# Get single country
curl http://localhost:5000/countries/Nigeria

# Delete country
curl -X DELETE http://localhost:5000/countries/Nigeria

# Get status
curl http://localhost:5000/status

# Download summary image
curl http://localhost:5000/countries/image --output summary.png
Using Python Requests
pythonimport requests

base_url = "http://localhost:5000"

# Refresh
response = requests.post(f"{base_url}/countries/refresh")
print(response.json())

# Get countries
response = requests.get(f"{base_url}/countries?region=Africa")
print(response.json())

# Get status
response = requests.get(f"{base_url}/status")
print(response.json())
Deployment
Recommended Platforms

Railway - Easy deployment with automatic MySQL provisioning
AWS EC2 - Full control with RDS for MySQL
Heroku - Simple deployment with ClearDB MySQL addon
DigitalOcean App Platform - Managed deployment with database

Production Considerations

Environment Variables:

Set FLASK_ENV=production
Use strong database credentials
Configure proper API timeouts


Database:

Enable connection pooling
Set up proper indexes
Regular backups


Security:

Use HTTPS
Implement rate limiting
Add authentication if needed
Sanitize inputs


Monitoring:

Log errors to file or service
Monitor API response times
Track database performance


Gunicorn for Production:

bashgunicorn -w 4 -b 0.0.0.0:5000 run:app
Database Schema
sqlCREATE TABLE countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    capital VARCHAR(255),
    region VARCHAR(100),
    population BIGINT NOT NULL,
    currency_code VARCHAR(10),
    exchange_rate DECIMAL(15, 6),
    estimated_gdp DECIMAL(20, 2),
    flag_url TEXT,
    last_refreshed_at TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_region (region),
    INDEX idx_currency (currency_code)
);
Troubleshooting
Database Connection Issues
bash# Check MySQL is running
sudo systemctl status mysql

# Test connection
mysql -u root -p -e "SELECT 1"
Module Not Found Errors
bash# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
External API Timeout

Check internet connection
Increase API_TIMEOUT in .env
Verify API URLs are accessible

Image Generation Fails

Ensure cache/ directory exists
Check Pillow installation: pip install Pillow
Verify font paths for your OS

Contributing

Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Create a Pull Request

License
MIT License - feel free to use this project for learning or commercial purposes.
Contact
For issues or questions, please open an issue on GitHub.

Built with ❤️ using Python & Flask