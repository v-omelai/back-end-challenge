from flask_restx import fields

from app import api

color = api.model('Color', {
    'key': fields.String(required=True, description='Color key'),
    'name': fields.String(required=True, description='Color name'),
    'created': fields.DateTime(description='Creation date'),
})

colors = api.model('Colors', {
    'colors': fields.List(fields.Nested(color, description='List of colors')),
})
