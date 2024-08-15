#!/usr/bin/python3
"""Flask app to control API"""
from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from backend.models import storage
from flask_cors import CORS
from api.v1.views import app_views
from dotenv import load_dotenv
from os import getenv
from backend.models.user import User


load_dotenv()


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error):
	"""catches any 404 error"""
	return make_response(jsonify({'error': 'Not found, try to login'}), 404)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", threaded=True, debug=True)
