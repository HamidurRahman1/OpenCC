
from edu.lagcc.occ.singletons.flask_instance import SingletonFlaskInstance
from edu.lagcc.occ.singletons.mysql_instance import SingletonMySQLInstance

app = SingletonFlaskInstance.get_instance()
mysql = SingletonMySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    cur.execute("show tables")
    for i in cur.fetchall():
        print(i)
    cur.execute("select * from terms")
    for i in cur.fetchall():
        print(i)
    cur.close()
    return "my home page 1"


if __name__ == "__main__":

    app.run()



