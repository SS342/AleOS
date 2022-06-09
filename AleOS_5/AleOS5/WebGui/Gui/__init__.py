from flask import Flask

from Gui.home import home_routers


def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_routers)

    return app
