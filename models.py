from flask_restx import fields

from app import api

category = api.model('Category', {
    'id': fields.Integer(required=True, description='Category ID'),
    'name': fields.String(required=True, description='Category name'),
})

categories = api.model('Categories', {
    'categories': fields.List(fields.Nested(category, description='List of categories')),
})

color = api.model('Color', {
    'id': fields.Integer(required=True, description='Color ID'),
    'name': fields.String(required=True, description='Color name'),
})

colors = api.model('Colors', {
    'colors': fields.List(fields.Nested(color, description='List of colors')),
})

product = api.model('Product', {
    'id': fields.Integer(required=True, description='Product ID'),
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(description='Product description'),
    'amount': fields.Integer(description='Product amount'),
    'category': fields.Nested(category, description='Product category'),
    'color': fields.Nested(color, description='Product color'),
    'created': fields.DateTime(description='Creation date'),
})

products = api.model('Products', {
    'products': fields.List(fields.Nested(product, description='List of products')),
})
