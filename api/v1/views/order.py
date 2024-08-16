#!/usr/bin/python3

from flask_jwt_extended import jwt_required
from api.v1.views import app_views
from api.v1.utils.authorization import role_required
from backend.models import storage
from backend.models.order import Order
from backend.models.shoe import Shoe
from flask import jsonify, request
from api.v1.utils.authorization import get_current_user


@app_views.route('/orders', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def get_allOrders():
    """Returns JSON format of all orders"""
    list_order = []
    orders = storage.all(Order).values()
    if not orders:
        return jsonify({'Error': 'No order available yet'})
    for order in orders:
        list_order.append(order.to_dict())
    return jsonify(list_order), 200

@app_views.route('/orders/<id>', methods=['GET'], strict_slashes=False)
def get_order_by_id(id):
    """Returns product based on id"""
    order_obj = storage.get(Order, id)
    if not order_obj:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order_obj.to_dict()), 200

@app_views.route('/checkout', methods=['POST'], strict_slashes=False)
@jwt_required()
def checkout():
    """Handle the checkout process."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Retrieve the user's cart
    cart = storage.get_cart_by_userId(user.id)
    if not cart or not cart.items:
        return jsonify({'error': 'Cart is empty'}), 400

    # Create an order
    order = Order(user_id=user.id, items=cart.items)
    order.calculate_total()
    order.status = "completed"
    storage.new(order)

    # Clear the user's cart
    storage.delete(cart)

    # Save changes to storage
    storage.save()

    # Process payment here (not implemented yet)

    return jsonify({'message': 'Checkout successful', 'order_id': order.id}), 200
