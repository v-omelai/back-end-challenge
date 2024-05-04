from flask_restx import reqparse

parser = reqparse.RequestParser()

LIST_CATEGORIES = parser.copy()
LIST_CATEGORIES.add_argument('name', type=str, required=False, help='Category name')

CREATE_CATEGORY = parser.copy()
CREATE_CATEGORY.add_argument('name', type=str, required=True, location='json')

UPDATE_CATEGORY = parser.copy()
UPDATE_CATEGORY.add_argument('name', type=str, required=False, location='json')
