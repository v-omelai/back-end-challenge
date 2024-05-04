from flask_restx import reqparse

parser = reqparse.RequestParser()

LIST_COLORS = parser.copy()
LIST_COLORS.add_argument('name', type=str, required=False, help='Color name')

CREATE_COLOR = parser.copy()
CREATE_COLOR.add_argument('name', type=str, required=True, location='json')

UPDATE_COLOR = parser.copy()
UPDATE_COLOR.add_argument('name', type=str, required=False, location='json')
