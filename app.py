from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Hello(Resource):
    def get(self):
        return jsonify({"message": "Hello World!"})

class Square(Resource):
    def get(self, num):
        return jsonify({'Shape': __class__.__name__,
                        'Area': num*num})

class Echo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('arg1', type=str, location='args')
        parser.add_argument('arg2', type=str, location='args')

        arguments = parser.parse_args()

        return jsonify(arguments)

api.add_resource(Hello, '/')
api.add_resource(Square, "/square/<int:num>")
api.add_resource(Echo, "/echo")

if __name__ == "__main__":
    app.run(debug=True)

