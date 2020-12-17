
from flask import Flask
from edu.lagcc.occ.config.starter import APP_NAME

app = Flask(__name__)
app.name = APP_NAME


@app.route('/', methods=['GET'])
def index():
    return "home page"


if __name__ == "__main__":

    app.config.from_pyfile('edu/lagcc/occ/config/config.py')
    app.run()

    print(app.config.get("MYSQL_HOST"))
    print(app.config.get("MYSQL_USER"))
    print(app.config.get("MYSQL_DB"))

    term = "2021 Spring"
    subject_code = "VETE"
    class_num_5_digit = "55576"
