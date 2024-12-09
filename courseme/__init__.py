import os

from flask import Flask

# References
# - Used Flask documentation to get webpage setup, https://flask.palletsprojects.com/en/stable/tutorial/

def create_app(test_config=None):
    # Creates and configures the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'courseme.sqlite'),
    )

    if test_config is None:
        # When not testing, loads the instance config if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Loads the test config if passed in
        app.config.from_mapping(test_config)

    # Ensures that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import courses
    app.register_blueprint(courses.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app