import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', #random value for deploiements
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    from . import db
    from . import auth
    from . import blog
    
    db.init_app(app)
    
    #import the bluepritn
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index')
    
    @app.route('/hello', methods=('GET','POST'))
    def hello():
        return b'Hello, World!'
    

   
    return app