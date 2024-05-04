from flask_restx import fields

from app import api
from models.categories import category
from models.colors import color

product = api.model('Product', {
    'key': fields.String(required=True, description='Product key'),
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
