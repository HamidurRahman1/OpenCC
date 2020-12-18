
from flask import Flask
from flask_mysqldb import MySQL
from edu.lagcc.occ.config.starter import APP_NAME

app = Flask(__name__)
app.name = APP_NAME

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    cur.execute("show tables")
    for i in cur.fetchall():
        print(i)
    cur.close()
    return "home page"


if __name__ == "__main__":

    app.config.from_pyfile('edu/lagcc/occ/config/config.py')
    app.run()

