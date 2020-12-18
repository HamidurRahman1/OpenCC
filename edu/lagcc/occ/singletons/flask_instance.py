
from flask import Flask
from edu.lagcc.occ.config.starter import APP_NAME


class SingletonFlaskInstance:

    __app_instance = None

    def __init__(self):
        if SingletonFlaskInstance.__app_instance is None:
            SingletonFlaskInstance.__app_instance = Flask(__name__)
            SingletonFlaskInstance.__app_instance.name = APP_NAME
            SingletonFlaskInstance.__app_instance.config.from_pyfile("../config/config.py")

    @staticmethod
    def get_instance():
        if SingletonFlaskInstance.__app_instance is None:
            SingletonFlaskInstance()
        return SingletonFlaskInstance.__app_instance


