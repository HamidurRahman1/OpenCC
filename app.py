
from edu.lagcc.occ.services.term_service import TermService
from edu.lagcc.occ.singletons.flask_instance import SingletonFlaskInstance
from edu.lagcc.occ.singletons.mysql_instance import SingletonMySQLInstance


if __name__ == "__main__":

    app = SingletonFlaskInstance.get_instance()
    mysql = SingletonMySQLInstance.get_instance()


    @app.route('/', methods=['GET'])
    def index():
        ts = TermService(mysql.connection)
        for t in ts.get_all_terms():
            print(t)
        print(ts.get_term_by_name("2025 Spring"))
        return "my home page 1"

    app.run()



