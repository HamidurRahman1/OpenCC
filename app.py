
from edu.lagcc.occ.singletons.flask_instance import SingletonFlaskInstance

app = SingletonFlaskInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    # cur = mysql.connection.cursor()
    # cur.execute("show tables")
    # for i in cur.fetchall():
    #     print(i)
    # cur.close()
    return "my home page 1"


if __name__ == "__main__":

    app.run()



