from flask_restx import fields

from app import api

category = api.model('Category', {
    'key': fields.String(required=True, description='Category key'),
    'name': fields.String(required=True, description='Category name'),
    'created': fields.DateTime(description='Creation date'),
})

categories = api.model('Categories', {
    'categories': fields.List(fields.Nested(category, description='List of categories')),
})
