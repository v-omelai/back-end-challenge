from app import api

categories = api.namespace('categories', description='Category operations')
colors = api.namespace('colors', description='Color operations')
products = api.namespace('products', description='Product operations')
