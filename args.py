from flask_restx import reqparse

rp = reqparse.RequestParser()


class Products:
    @staticmethod
    def get():
        parser = rp.copy()
        parser.add_argument('name', type=str, required=False, help='Product name')
        return parser

    @staticmethod
    def create():
        parser = rp.copy()
        parser.add_argument('name', type=str, required=True, location='json')
        parser.add_argument('description', type=str, required=True, location='json')
        parser.add_argument('amount', type=int, required=True, location='json')
        parser.add_argument('category', type=int, required=True, location='json')
        parser.add_argument('color', type=int, required=True, location='json')
        return parser


class Product:
    @staticmethod
    def patch():
        parser = rp.copy()
        parser.add_argument('name', type=str, required=False, location='json')
        parser.add_argument('description', type=str, required=False, location='json')
        parser.add_argument('amount', type=int, required=False, location='json')
        parser.add_argument('category', type=int, required=False, location='json')
        parser.add_argument('color', type=int, required=False, location='json')
        return parser
