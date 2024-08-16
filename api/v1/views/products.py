#!/usr/bin/python3
from api.v1.views import app_views
from backend.models import storage
from backend.models.shoe import Shoe
from flask import jsonify, abort, request
from flask_jwt_extended import jwt_required
from api.v1.utils.authorization import role_required


@app_views.route('/products', methods=['GET'], strict_slashes=False)
def get_products():
    """Returns JSON format of all products"""
    list_products = []
    products = storage.all(Shoe).values()
    if not products:
        abort(404)
    for prods in products:
        list_products.append(prods.to_dict())
    return jsonify(list_products), 200

@app_views.route('/products/<id>', methods=['GET'], strict_slashes=False)
def get_productById(id):
    """Returns product based on id"""
    shoe_obj = storage.get(Shoe, id)
    if not shoe_obj:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(shoe_obj.to_dict()), 200

@app_views.route('/products', methods=['POST'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def create_product():
    data = request.get_json()
    try:
        new_product = Shoe(**data)
        storage.new(new_product)
        storage.save()
        return jsonify(new_product.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app_views.route('/products/<id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def update_product(id):
    data = request.get_json()
    product = storage.get(Shoe, id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Update product fields
    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    storage.save()
    return jsonify(product.to_dict()), 200

@app_views.route('/products/<id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def delete_product(id):
    product = storage.get(Shoe, id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    storage.delete(product)
    storage.save()
    return jsonify({'message': 'Product deleted successfully'}), 200
