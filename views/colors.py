import json
import uuid
from datetime import datetime, timezone

from flask_restx import Resource
from werkzeug.exceptions import BadRequest, NotFound

import models
import namespaces
import parsers

from app import api, redis

redis.set('colors', json.dumps({}))


@namespaces.colors.route('/')
class ColorsView(Resource):
    @api.expect(parsers.LIST_COLORS)
    @api.marshal_with(models.colors)
    def get(self):
        colors = json.loads(redis.get('colors'))
        args = parsers.LIST_COLORS.parse_args()
        if name := args['name']:
            values = [value for value in colors.values() if name in value['name']]
        else:
            values = [*colors.values()]
        return {'colors': values}

    @api.expect(parsers.CREATE_COLOR)
    @api.marshal_with(models.color)
    def post(self):
        try:
            colors = json.loads(redis.get('colors'))
            args = parsers.CREATE_COLOR.parse_args()
            key = str(uuid.uuid4())
            color = {
                'key': key,
                'name': args['name'],
                'created': datetime.now(timezone.utc).isoformat(),
            }
            colors[key] = color
            redis.set('colors', json.dumps(colors))
            return color
        except KeyError as exc:
            raise BadRequest from exc


@namespaces.colors.route('/<key>')
class ColorView(Resource):
    @api.marshal_with(models.color)
    def get(self, key: str):
        try:
            colors = json.loads(redis.get('colors'))
            color = colors[key]
            return color
        except KeyError as exc:
            raise NotFound from exc

    @api.expect(parsers.UPDATE_COLOR)
    @api.marshal_with(models.color)
    def patch(self, key: str):
        try:
            colors = json.loads(redis.get('colors'))
            args = parsers.UPDATE_COLOR.parse_args()
            color = colors[key]
            if name := args['name']:
                color['name'] = name
            redis.set('colors', json.dumps(colors))
            return color
        except KeyError as exc:
            raise BadRequest from exc

    @api.marshal_with(models.color)
    def delete(self, key: str):
        try:
            colors = json.loads(redis.get('colors'))
            color = colors.pop(key)
            redis.set('colors', json.dumps(colors))
            return color
        except KeyError as exc:
            raise NotFound from exc
