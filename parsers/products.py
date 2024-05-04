from flask_restx import reqparse

parser = reqparse.RequestParser()

LIST_PRODUCTS = parser.copy()
LIST_PRODUCTS.add_argument('name', type=str, required=False, help='Product name')

CREATE_PRODUCT = parser.copy()
CREATE_PRODUCT.add_argument('name', type=str, required=True, location='json')
CREATE_PRODUCT.add_argument('description', type=str, required=True, location='json')
CREATE_PRODUCT.add_argument('amount', type=int, required=True, location='json')
CREATE_PRODUCT.add_argument('categoryKey', type=str, required=True, location='json')
CREATE_PRODUCT.add_argument('colorKey', type=str, required=True, location='json')

UPDATE_PRODUCT = parser.copy()
UPDATE_PRODUCT.add_argument('name', type=str, required=False, location='json')
UPDATE_PRODUCT.add_argument('description', type=str, required=False, location='json')
UPDATE_PRODUCT.add_argument('amount', type=int, required=False, location='json')
UPDATE_PRODUCT.add_argument('categoryKey', type=str, required=False, location='json')
UPDATE_PRODUCT.add_argument('colorKey', type=str, required=False, location='json')
