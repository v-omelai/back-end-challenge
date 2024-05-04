from datetime import datetime, timezone

from flask_restx import Resource
from werkzeug.exceptions import NotFound, BadRequest

import args
import models
import namespaces
from app import api
from data import Categories, Colors, Products

categories, colors, products = Categories.DICT, Colors.DICT, Products.DICT


@namespaces.categories.route('/')
class CategoriesView(Resource):
    @api.marshal_with(models.categories)
    def get(self):
        return {'categories': [*categories.values()]}


@namespaces.colors.route('/')
class ColorsView(Resource):
    @api.marshal_with(models.colors)
    def get(self):
        return {'colors': [*colors.values()]}


@namespaces.products.route('/')
class ProductsView(Resource):
    @api.expect(args.Products.get())
    @api.marshal_with(models.products)
    def get(self):
        arguments = args.Products.get().parse_args()
        if name := arguments['name']:
            values = [value for value in products.values() if name in value['name']]
        else:
            values = [*products.values()]
        return {'products': values}

    @api.expect(args.Products.create())
    @api.marshal_with(models.product)
    def post(self):
        try:
            arguments = args.Products.create().parse_args()
            id_ = max(products.keys()) + 1  # noqa
            product = {
                'id': id_,
                'name': arguments['name'],
                'description': arguments['description'],
                'amount': arguments['amount'],
                'category': categories[arguments['category']],
                'color': colors[arguments['color']],
                'created': datetime.now(timezone.utc).isoformat(),
            }
            products[id_] = product
            return product
        except KeyError as exc:
            raise BadRequest from exc


@namespaces.products.route('/<int:id_>')
class ProductView(Resource):
    @api.marshal_with(models.product)
    def get(self, id_: int):  # noqa
        try:
            product = products[id_]
            return product
        except KeyError as exc:
            raise NotFound from exc

    @api.expect(args.Product.patch())
    @api.marshal_with(models.product)
    def patch(self, id_: int):  # noqa
        try:
            arguments = args.Product.patch().parse_args()
            product = products[id_]
            if name := arguments['name']:
                product['name'] = name
            if description := arguments['description']:
                product['description'] = description
            if amount := arguments['amount']:
                product['amount'] = amount
            if category := arguments['category']:
                product['category'] = categories[category]
            if color := arguments['color']:
                product['color'] = colors[color]
            return product
        except KeyError as exc:
            raise BadRequest from exc

    @api.marshal_with(models.product)
    def delete(self, id_: int):  # noqa
        try:
            product = products.pop(id_)
            return product
        except KeyError as exc:
            raise NotFound from exc


@namespaces.products.route('/<int:id_>/increase-amount')
class ProductIncreaseAmountView(Resource):
    @api.marshal_with(models.product)
    def post(self, id_: int):  # noqa
        try:
            product = products[id_]
            product['amount'] += 1
            return product
        except KeyError as exc:
            raise BadRequest from exc
