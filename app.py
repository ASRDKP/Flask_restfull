from flask import Flask, redirect, request
from flask_restful import Api, Resource,reqparse, abort

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get (self):
        return {'data' : 'Hello World'}
    
class HelloName(Resource):
    def get (self, name):
        return {'data' : 'Hello {}'.format(name)}
       
    
api.add_resource(HelloWorld,"/")
api.add_resource(HelloName,"/<string:name>")

if __name__ == '__main__':
    app.run(debug=True)

