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

app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
	SWAGGER_URL,
	API_URL,
	config={
		'app_name': 'JWS Collections APi'
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.errorhandler(404)
def not_found(error):
	"""catches any 404 error"""
	return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", threaded=True, debug=True)
