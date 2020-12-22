
from flask import Flask
from edu.lagcc.occ.config.starter import APP_NAME
from edu.lagcc.occ.controller.controller import home


class FlaskInstance:

    __app_instance = None

    def __init__(self):
        if FlaskInstance.__app_instance is None:
            FlaskInstance.__app_instance = Flask(__name__)
            FlaskInstance.__app_instance.name = APP_NAME
            FlaskInstance.__app_instance.config.from_pyfile("../config/config.py")
            FlaskInstance.__app_instance.register_blueprint(home)

    @staticmethod
    def get_instance():
        if FlaskInstance.__app_instance is None:
            FlaskInstance()
        return FlaskInstance.__app_instance


