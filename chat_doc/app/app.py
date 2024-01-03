import os
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from chat_doc.app.routes import routes_blueprint
from chat_doc.config import BASE_DIR, config, logger


class App:
    def __init__(self, config=config["flask_app"]):
        self.app = Flask(
            config["app_name"],
            static_url_path="/static/",
            template_folder=BASE_DIR + "/app/templates",
        )
        self.configure_app(config)
        self.db = SQLAlchemy(self.app)
        self.register_blueprints()
        os.environ["TZ"] = "Europe/Berlin"

    def configure_app(self, config):
        self.app.config["FLASK_SECRET"] = config["secret"]
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + config["db_name"]
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    def register_blueprints(self):
        self.app.register_blueprint(routes_blueprint)

    def run(self, port=5000, debug=True):
        self.app.run(port=port, debug=debug)
        logger.log(f"App listening on part {port}")
