from flask import (
    Blueprint, g, request, jsonify
)
from app.db import get_db
from app.auth import login_required
from app.models import Order  # Import the Order class

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()
    body = data.get('body')
    db = get_db()
    error = None

    if not body:
        error = 'Order body is required.'

    if error is None:
        db.execute(
            "INSERT INTO orders (user_id, body) VALUES (?, ?)",
            (g.user['id'], body),
        )
        db.commit()
        order_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        order = Order(order_id, g.user['id'], body)
        return jsonify({"message": "Order created successfully", "order": order.to_dict()}), 201

    return jsonify({"error": error}), 400

@bp.route('/', methods=['GET'])
@login_required
def get_orders():
    db = get_db()
    orders = db.execute(
        'SELECT * FROM orders WHERE user_id = ?', (g.user['id'],)
    ).fetchall()
    order_list = [Order(order['id'], order['user_id'], order['body']).to_dict() for order in orders]
    return jsonify(order_list), 200

@bp.route('/<int:order_id>', methods=['PUT'])
@login_required
def update_order(order_id):
    data = request.get_json()
    body = data.get('body')
    db = get_db()
    error = None

    if not body:
        error = 'Order body is required.'

    if error is None:
        db.execute(
            "UPDATE orders SET body = ? WHERE id = ? AND user_id = ?",
            (body, order_id, g.user['id']),
        )
        db.commit()
        order = Order(order_id, g.user['id'], body)
        return jsonify({"message": "Order updated successfully", "order": order.to_dict()}), 200

    return jsonify({"error": error}), 400

@bp.route('/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    db = get_db()
    db.execute(
        "DELETE FROM orders WHERE id = ? AND user_id = ?",
        (order_id, g.user['id']),
    )
    db.commit()
    return jsonify({"message": "Order deleted successfully"}), 200