#!/usr/bin/python3
"""Route to handle cart"""
from flask_jwt_extended import jwt_required
from api.v1.views import app_views
from api.v1.utils.authorization import role_required
from backend.models import storage
from backend.models.cart import Cart
from backend.models.shoe import Shoe
from flask import jsonify, request, abort
from api.v1.utils.authorization import get_current_user


@app_views.route('/carts', methods=['GET', 'OPTIONS'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def get_allCarts():
    """Retrieves all carts of users

    Returns:
        json (list): A list containing all carts
    """
    try:
        list_carts = []
        carts = storage.all(Cart).values()
        if not carts:
            return jsonify({'Error': 'No cart available in database'})
        for cart in carts:
            list_carts.append(cart.to_dict())
        return jsonify(list_carts), 200
    except Exception:
        abort(500)


@app_views.route('/carts/<id>', methods=['GET'], strict_slashes=False)
def get_cart_by_id(id: str):
    """Retrieves Cart based on id

    Args:
        id (str): the cart's id

    Returns:
        json(dict): json dictionary repr of the Cart
    """
    try:
        cart_obj = storage.get(Cart, id)
        if not cart_obj:
            return jsonify({'error': 'Cart not found'}), 404
        return jsonify(cart_obj.to_dict()), 200
    except Exception:
        abort(500)


@app_views.route('/cart', methods=['GET', 'OPTIONS'], strict_slashes=False)
@jwt_required()
def get_user_cart():
    """Retrieves current user cart

    Returns:
        json(dict): json dictionary repr of the Cart
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        cart = storage.get_cart_by_userId(user.id)
        if not cart:
            return jsonify({'message': 'Cart is empty'}), 200

        return jsonify(cart.to_dict()), 200
    except Exception:
        abort(500)


@app_views.route('/cart/add', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_to_cart():
    """Adds an item to cart

    {
       shoe_id: 283928-238-dw939
       quantity: 2
    }

    Returns:
        json: success | failed
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    shoe_id = data.get('shoe_id')
    quantity = int(data.get('quantity', 1))

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
