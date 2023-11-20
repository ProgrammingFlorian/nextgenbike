from flask import Flask
from flask_cors import CORS

import app.routes as routes
from app.config import Config
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    CORS(app)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(routes.url)


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=80)
