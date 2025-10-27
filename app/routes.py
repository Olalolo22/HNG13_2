from flask import Blueprint, jsonify, request, send_file
from app.services.country_service import CountryService
from app.config import Config
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/countries/refresh', methods=['POST'])
def refresh_countries():
    """Fetch and cache all countries and exchange rates"""
    try:
        count = CountryService.fetch_and_refresh()
        return jsonify({
            "message": "Countries refreshed successfully",
            "count": count
        }), 200
        
    except Exception as e:
        error_message = str(e)
        if "REST Countries API" in error_message:
            return jsonify({
                "error": "External data source unavailable",
                "details": error_message
            }), 503
        elif "Exchange Rate API" in error_message:
            return jsonify({
                "error": "External data source unavailable",
                "details": error_message
            }), 503
        else:
            return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/countries', methods=['GET'])
def get_countries():
    """Get all countries with optional filters and sorting"""
    try:
        region = request.args.get('region')
        currency = request.args.get('currency')
        sort = request.args.get('sort')
        
        countries = CountryService.get_countries(
            region=region,
            currency=currency,
            sort=sort
        )
        
        return jsonify(countries), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/countries/<string:name>', methods=['GET'])
def get_country(name):
    """Get single country by name"""
    try:
        # Special case: if name is 'image', serve the summary image
        if name.lower() == 'image':
            print(f"Image route triggered. Path: {Config.IMAGE_PATH}")
            print(f"File exists: {os.path.exists(Config.IMAGE_PATH)}")
            if not os.path.exists(Config.IMAGE_PATH):
                return jsonify({"error": "Summary image not found"}), 404
            return send_file(Config.IMAGE_PATH, mimetype='image/png')
        
        country = CountryService.get_country_by_name(name)
        
        if not country:
            return jsonify({"error": "Country not found"}), 404
        
        return jsonify(country), 200
        
    except Exception as e:
        print(f"Error in get_country: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/countries/<string:name>', methods=['DELETE'])
def delete_country(name):
    """Delete country by name"""
    try:
        deleted = CountryService.delete_country(name)
        
        if not deleted:
            return jsonify({"error": "Country not found"}), 404
        
        return jsonify({"message": f"Country '{name}' deleted successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/status', methods=['GET'])
def get_status():
    """Get API status with total countries and last refresh timestamp"""
    try:
        status = CountryService.get_status()
        return jsonify(status), 200
        
    except Exception as e:
        print(f"Status error: {e}")
        return jsonify({"error": "Internal server error"}), 500