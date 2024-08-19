#!/usr/bin/python3
"""Route to handle orders and checkout"""
from flask_jwt_extended import jwt_required
from api.v1.views import app_views
from api.v1.utils.authorization import role_required
from backend.models import storage
from backend.models.order import Order
from flask import jsonify, abort
from api.v1.utils.authorization import get_current_user


@app_views.route('/orders', methods=['GET'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def get_allOrders():
    """Retrieves all orders created

    Returns:
        json (list): list of all orders
    """
    try:
        list_order = []
        orders = storage.all(Order).values()
        if not orders:
            return jsonify({'Error': 'No order available yet'})
        for order in orders:
            list_order.append(order.to_dict())
        return jsonify(list_order), 200
    except Exception:
        abort(500)


@app_views.route('/orders/<id>', methods=['GET'], strict_slashes=False)
def get_order_by_id(id):
    """Get order by id

    Args:
        id (str): the id of the order

    Returns:
        json(dict): dictionary repr of the order
    """
    try:
        order_obj = storage.get(Order, id)
        if not order_obj:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify(order_obj.to_dict()), 200
    except Exception:
        abort(500)


@app_views.route('/checkout', methods=['POST'], strict_slashes=False)
@jwt_required()
def checkout():
    """Handle checkout of user

    Returns:
        json: success or failure
    """
    try:
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

        # Save changes to storage
        storage.save()

        # Process payment here (not implemented yet)

        return jsonify({'message': 'Checkout successful', 'order_id': order.id}), 200
    except Exception:
        abort(500)
