import os
from flask import Flask, jsonify, request
from . import db
from . import auth
from . import order 

# flask --app app init-db
# flask --app app run

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # db
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    # for the db path or mkdir ./instance
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # if testing and need a different config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # routes
    @app.route('/hello')
    def hello():
        return jsonify({'message': 'Hello, World!'})
    
    # initialize things
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(order.bp)

    return app