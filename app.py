
from edu.lagcc.occ.factory.flask_factory import FlaskFactoryInstance

app = FlaskFactoryInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    # cur = mysql.connection.cursor()
    # cur.execute("show tables")
    # for i in cur.fetchall():
    #     print(i)
    # cur.close()
    return "my home page"


if __name__ == "__main__":

    app.run()



