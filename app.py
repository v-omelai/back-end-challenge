from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app)

from views import *  # noqa

if __name__ == '__main__':
    app.run(debug=True)
