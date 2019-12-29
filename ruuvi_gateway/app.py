import os
from flask import Flask
from flask_basicauth import BasicAuth
from ruuvi_gateway.blueprints.v3_blueprint import v3_blueprint

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(v3_blueprint, url_prefix='/v3')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    basic_auth = BasicAuth(app)
        
    # a simple page that says hello
    @app.route('/heartbeat')
    def hello():
        return "Yes, everything's fine mate!"

    return app
