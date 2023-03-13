from flask import Flask, redirect, request
from flask_restful import Api, Resource,reqparse, abort

app = Flask(__name__)
api = Api(app)

register = {
    1 : {'name' : 'Rahul', 'lname' : 'Prajapat'},
    2 : {'name' : 'Ishita', 'lname' : 'Sakhala'},
    3 : {'name' : 'Khushhal', 'lname' : 'Gupta'}
}



class HelloWorld(Resource):
    def get (self):
        return {'data' : 'Hello World'}
    
class HelloName(Resource):
    def get (self, name):
        return {'data' : 'Hello {}'.format(name)}
    
    
class RegisterList(Resource):
    def get(self):
        return register


    
api.add_resource(HelloWorld,"/")
api.add_resource(HelloName,"/<string:name>")
api.add_resource(RegisterList,"/RegisterList")

if __name__ == '__main__':
    app.run(debug=True)

