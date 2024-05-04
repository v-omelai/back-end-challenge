import json
import uuid
from datetime import datetime, timezone

from flask_restx import Resource
from werkzeug.exceptions import BadRequest, NotFound

import models
import namespaces
import parsers

from app import api, redis

redis.set('products', json.dumps({}))


@namespaces.products.route('/')
class ProductsView(Resource):
    @api.expect(parsers.LIST_PRODUCTS)
    @api.marshal_with(models.products)
    def get(self):
        products = json.loads(redis.get('products'))
        args = parsers.LIST_PRODUCTS.parse_args()
        if name := args['name']:
            values = [value for value in products.values() if name in value['name']]
        else:
            values = [*products.values()]
        return {'products': values}

    @api.expect(parsers.CREATE_PRODUCT)
    @api.marshal_with(models.product)
    def post(self):
        try:
            products = json.loads(redis.get('products'))
            categories = json.loads(redis.get('categories'))
            colors = json.loads(redis.get('colors'))
            args = parsers.CREATE_PRODUCT.parse_args()
            key = str(uuid.uuid4())
            product = {
                'key': key,
                'name': args['name'],
                'description': args['description'],
                'amount': args['amount'],
                'category': categories[args['categoryKey']],
                'color': colors[args['colorKey']],
                'created': datetime.now(timezone.utc).isoformat(),
            }
            products[key] = product
            redis.set('products', json.dumps(products))
            return product
        except KeyError as exc:
            raise BadRequest from exc


@namespaces.products.route('/<key>')
class ProductView(Resource):
    @api.marshal_with(models.product)
    def get(self, key: str):
        try:
            products = json.loads(redis.get('products'))
            product = products[key]
            return product
        except KeyError as exc:
            raise NotFound from exc

    @api.expect(parsers.UPDATE_PRODUCT)
    @api.marshal_with(models.product)
    def patch(self, key: str):
        try:
            products = json.loads(redis.get('products'))
            categories = json.loads(redis.get('categories'))
            colors = json.loads(redis.get('colors'))
            args = parsers.UPDATE_PRODUCT.parse_args()
            product = products[key]
            if name := args['name']:
                product['name'] = name
            if description := args['description']:
                product['description'] = description
            if amount := args['amount']:
                product['amount'] = amount
            if category := args['categoryKey']:
                product['category'] = categories[category]
            if color := args['colorKey']:
                product['color'] = colors[color]
            redis.set('products', json.dumps(products))
            return product
        except KeyError as exc:
            raise BadRequest from exc

    @api.marshal_with(models.product)
    def delete(self, key: str):
        try:
            products = json.loads(redis.get('products'))
            product = products.pop(key)
            redis.set('products', json.dumps(products))
            return product
        except KeyError as exc:
            raise NotFound from exc


@namespaces.products.route('/<key>/increase-amount')
class ProductIncreaseAmountView(Resource):
    @api.marshal_with(models.product)
    def post(self, key: str):
        try:
            products = json.loads(redis.get('products'))
            product = products[key]
            product['amount'] += 1
            redis.set('products', json.dumps(products))
            return product
        except KeyError as exc:
            raise BadRequest from exc
