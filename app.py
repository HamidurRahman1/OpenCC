
from edu.lagcc.occ.repositories.request_repo import RequestRepository
from edu.lagcc.occ.searcher.class_searcher import OpenClassSearcher
from edu.lagcc.occ.instances.flask_instance import FlaskInstance
from edu.lagcc.occ.instances.mysql_instance import MySQLInstance
from os import environ
from flask import current_app

app = FlaskInstance.get_instance()
mysql = MySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    r = next(iter(RequestRepository(mysql.connection).get_requests_to_search_and_notify()[38553]))
    print(r)
    obj = OpenClassSearcher(r.term.term_name, r.subject.subject_code, r.class_num_5_digit).check_session_one()
    if obj.found:
        if obj.status:
            print(obj.status, "found in session 1")
    else:
        obj.check_session_two()
        if obj.found:
            if obj.status:
                print(obj.status, "found in session 2")
    return "home"


if __name__ == "__main__":

    app.run()



