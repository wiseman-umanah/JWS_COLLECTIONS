#!/usr/bin/python3

from flask_jwt_extended import jwt_required
from api.v1.views import app_views
from api.v1.utils.authorization import role_required
from backend.models import storage
from backend.models.cart import Cart
from backend.models.cartitem import CartItem
from backend.models.shoe import Shoe
from flask import jsonify, request
from api.v1.utils.authorization import get_current_user

@app_views.route('/carts', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def get_allCarts():
    """Returns JSON format of all carts"""
    list_carts = []
    carts = storage.all(Cart).values()
    if not carts:
        return jsonify({'Error': 'No cart available in database'})
    for cart in carts:
        list_carts.append(cart.to_dict())
    return jsonify(list_carts), 200

@app_views.route('/carts/<id>', methods=['GET'], strict_slashes=False)
def get_cart_by_id(id):
    """Returns product based on id"""
    cart_obj = storage.get(Cart, id)
    if not cart_obj:
        return jsonify({'error': 'Cart not found'}), 404
    return jsonify(cart_obj.to_dict()), 200

@app_views.route('/cart', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_cart():
    """Retrieve the current user's cart"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    cart = storage.get_cart_by_userId(user.id)
    if not cart:
        return jsonify({'message': 'Cart is empty'}), 200
    
    return jsonify(cart.to_dict()), 200

@app_views.route('/cart/add', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_to_cart():
    """Add an item to the current user's cart"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    shoe_id = data.get('shoe_id')
    quantity = data.get('quantity', 1)
    
    # Retrieve the shoe
    shoe = storage.get(Shoe, shoe_id)
    if not shoe:
        return jsonify({'error': 'Shoe not found'}), 404
    
    # Retrieve or create the cart
    cart = storage.get_cart_by_userId(user.id)
    if not cart:
        cart = Cart(user_id=user.id)
        storage.new(cart)
    
    cart.add_item(shoe_name=shoe.shoe_name,
                  shoe_id=shoe.id, quantity=quantity,
                  price=shoe.shoe_price)
    
    storage.save()
    
    return jsonify({'message': 'Item added to cart successfully'}), 200
