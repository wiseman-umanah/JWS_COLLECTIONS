#!/usr/bin/python3
from api.v1.views import app_views
from backend.models import storage
from backend.models.shoe import Shoe
from flask import jsonify, abort
# from flask_jwt_extended import jwt_required


@app_views.route('/products', methods=['GET'], strict_slashes=False)
def get_products():
    """Returns JSON format of all products"""
    list_products = []
    products = storage.all(Shoe).values()
    if not products:
        abort(404)
    for prods in products:
        list_products.append(prods.to_dict())
    return jsonify(list_products)

@app_views.route('/products/<id>', methods=['GET'], strict_slashes=False)
def get_productById(id):
    """Returns product based on id"""
    shoe_obj = storage.get(Shoe, id)
    if not shoe_obj:
        return jsonify({'error': 'Product not found'})
    return jsonify(shoe_obj.to_dict())
