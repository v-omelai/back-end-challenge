import json
import uuid
from datetime import datetime, timezone

from flask_restx import Resource
from werkzeug.exceptions import BadRequest, NotFound

import models
import namespaces
import parsers

from app import api, redis

redis.set('categories', json.dumps({}))


@namespaces.categories.route('/')
class CategoriesView(Resource):
    @api.expect(parsers.LIST_CATEGORIES)
    @api.marshal_with(models.categories)
    def get(self):
        categories = json.loads(redis.get('categories'))
        args = parsers.LIST_CATEGORIES.parse_args()
        if name := args['name']:
            values = [value for value in categories.values() if name in value['name']]
        else:
            values = [*categories.values()]
        return {'categories': values}

    @api.expect(parsers.CREATE_CATEGORY)
    @api.marshal_with(models.category)
    def post(self):
        try:
            categories = json.loads(redis.get('categories'))
            args = parsers.CREATE_CATEGORY.parse_args()
            key = str(uuid.uuid4())
            category = {
                'key': key,
                'name': args['name'],
                'created': datetime.now(timezone.utc).isoformat(),
            }
            categories[key] = category
            redis.set('categories', json.dumps(categories))
            return category
        except KeyError as exc:
            raise BadRequest from exc


@namespaces.categories.route('/<key>')
class CategoryView(Resource):
    @api.marshal_with(models.category)
    def get(self, key: str):
        try:
            categories = json.loads(redis.get('categories'))
            category = categories[key]
            return category
        except KeyError as exc:
            raise NotFound from exc

    @api.expect(parsers.UPDATE_CATEGORY)
    @api.marshal_with(models.category)
    def patch(self, key: str):
        try:
            categories = json.loads(redis.get('categories'))
            args = parsers.UPDATE_CATEGORY.parse_args()
            category = categories[key]
            if name := args['name']:
                category['name'] = name
            redis.set('categories', json.dumps(categories))
            return category
        except KeyError as exc:
            raise BadRequest from exc

    @api.marshal_with(models.category)
    def delete(self, key: str):
        try:
            categories = json.loads(redis.get('categories'))
            category = categories.pop(key)
            redis.set('categories', json.dumps(categories))
            return category
        except KeyError as exc:
            raise NotFound from exc
