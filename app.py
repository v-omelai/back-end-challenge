from flask import Flask
from flask_restx import Api
from redis import Redis

import config

app = Flask(__name__)
api = Api(app)
redis = Redis.from_url(url=config.REDIS_URL)

from views import *  # noqa

if __name__ == '__main__':
    app.run(host='0.0.0.0')
