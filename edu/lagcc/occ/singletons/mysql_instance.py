
from flask_mysqldb import MySQL
from .flask_instance import SingletonFlaskInstance


class SingletonMySQLInstance:

    __mysql_instance = None

    def __init__(self):
        if SingletonMySQLInstance.__mysql_instance is None:
            SingletonMySQLInstance.__mysql_instance = MySQL(SingletonFlaskInstance.get_instance())

    @staticmethod
    def get_instance():
        if SingletonMySQLInstance.__mysql_instance is None:
            SingletonMySQLInstance()
        return SingletonMySQLInstance.__mysql_instance
