import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
import jwt
import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
    curl -X POST 'http://127.0.0.1:5000/auth/register?username=your_username&password=your_password'
    """
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return jsonify({"message": "User registered successfully"}), 201

        return jsonify({"error": error}), 400

@bp.route('/login', methods=('POST',))
def login():
    """
    curl -X POST 'http://127.0.0.1:5000/auth/login?username=eu&password=eu'
    """
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # token = jwt.encode({
            #     'user_id': user['id'],
            #     'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            # }, current_app.config['SECRET_KEY'], algorithm='HS256')
            token = jwt.encode({
                'user_id': user['id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, 'future_secret_key', algorithm='HS256')
            return jsonify({"token": token}), 200

        return jsonify({"error": error}), 400

@bp.before_app_request
def load_logged_in_user():
    token = request.headers.get('Authorization')

    if token is None:
        g.user = None
    else:
        try:
            data = jwt.decode(token, 'future_secret_key', algorithms=['HS256'])
            user_id = data['user_id']
            g.user = get_db().execute(
                'SELECT * FROM users WHERE id = ?', (user_id,)
            ).fetchone()
        except jwt.ExpiredSignatureError:
            g.user = None
        except jwt.InvalidTokenError:
            g.user = None

@bp.route('/logout', methods=('POST',))
def logout():
    """
    curl -X POST 'http://127.0.0.1:5000/auth/logout' -H 'Authorization: Bearer <your_token>'
    """
    token = request.headers.get('Authorization')
    if token:
        # Here you would normally blacklist the token or remove it from a token store
        return jsonify({"message": "Logout successful"}), 200
    return jsonify({"error": "No token provided"}), 400

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = request.headers.get('Authorization')
        print(token)
        if token is None:
            return jsonify({"error": "Authentication required"}), 401

        try:
            token = token.split(" ")[1] if " " in token else token
            data = jwt.decode(token, 'future_secret_key', algorithms=['HS256'])
            print(data)
            g.user = get_db().execute(
                'SELECT * FROM users WHERE id = ?', (data['user_id'],)
            ).fetchone()
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return view(**kwargs)

    return wrapped_view