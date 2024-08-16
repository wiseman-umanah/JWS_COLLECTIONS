#!/usr/bin/python3
from api.v1.views import app_views
from backend.models import storage
from backend.models.shoe import Shoe
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from api.v1.utils.authorization import role_required


@app_views.route('/products', methods=['GET'], strict_slashes=False)
def get_products():
    """Returns JSON format of all products"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    brand = request.args.get('brand')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    color = request.args.get('color')

    products = storage.all(Shoe).values()
    if not products:
        return jsonify({
            'page': page,
            'per_page': per_page,
            'total_products': 0,
            'total_pages': 0,
            'products': []
        }), 200
    
    # Apply filtering
    if category:
        products = [product for product in products if product.shoe_category == category]
    if brand:
        products = [product for product in products if product.shoe_brand == brand]
    if min_price is not None:
        products = [product for product in products if product.shoe_price >= min_price]
    if max_price is not None:
        products = [product for product in products if product.shoe_price <= max_price]
    if color:
        products = [product for product in products if product.shoe_color == color]

    # Calculate total pages ( page details )
    total_products = len(products)
    total_pages = (total_products + per_page - 1) // per_page

    # Paginate products
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = products[start:end]

    if start >= total_products:
        paginated_products = []

    response = {
        'page': page,
        'per_page': per_page,
        'total_products': total_products,
        'total_pages': total_pages,
        'products': [prods.to_dict() for prods in paginated_products]
    }
    
    return jsonify(response), 200

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
