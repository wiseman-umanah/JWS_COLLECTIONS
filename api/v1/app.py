#!/usr/bin/python3
"""Flask app to control API"""
from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from api.v1.views import app_views
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
import os

load_dotenv()

app = Flask(__name__)

# Ensure the secret key is fetched from the environment
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(app_views)

# Configure CORS
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Setup Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'JWS Collections API'
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 error

    Args:
        error (str): The error message

    Returns:
        json: Not found
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

# Consider adding more error handlers for better error reporting
@app.errorhandler(500)
def internal_error(error):
    """Handle 500 error

    Args:
        error (str): The error message

    Returns:
        json: Internal Server Error
    """
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
