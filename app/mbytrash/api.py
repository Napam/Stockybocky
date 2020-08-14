from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import random

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)


class RandNum(Resource):
    def get(self):
        return {'num':[random.randint(0,99)]}

class Product(Resource):
    def get(self):
        return {
            'product':[
                'Cat',
                'Dog'
            ]
        }

api.add_resource(RandNum, '/')
api.add_resource(Product, '/products')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)