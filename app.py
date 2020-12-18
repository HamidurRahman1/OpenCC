
from edu.lagcc.occ.services.term_service import TermService
from edu.lagcc.occ.singletons.flask_instance import SingletonFlaskInstance
from edu.lagcc.occ.singletons.mysql_instance import SingletonMySQLInstance


if __name__ == "__main__":

    app = SingletonFlaskInstance.get_instance()
    mysql = SingletonMySQLInstance.get_instance()


    @app.route('/', methods=['GET'])
    def index():
        for term in TermService(mysql.connection).get_all_terms():
            print(term)
        return "my home page 1"

    app.run()



