from flask import Flask, redirect, request, jsonify
from flask_restful import Api, Resource,reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root1234@localhost:3306/newhospitaldb'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

db.init_app(app)

# register = {
#     1 : {'name' : 'Rahul', 'lname' : 'Prajapat'},
#     2 : {'name' : 'Ishita', 'lname' : 'Sakhala'},
#     3 : {'name' : 'Khushhal', 'lname' : 'Gupta'}
# }
class register(db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    lname = db.Column(db.String(45), nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lname': self.lname
        }

with app.app_context():
    db.create_all()

class RegisterModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    
db.create_all()

class HelloWorld(Resource):
    def get (self):
        return {'data' : 'Hello World'}
    
class HelloName(Resource):
    def get (self, name):
        return {'data' : 'Hello {}'.format(name)}
    
    
class RegisterList(Resource):
    def get(self):
        return register


class Register(Resource):
    def get(self, Register_id):
        return register[Register_id]
    
    
    def post(self, Register_id):
        if Register_id in register:
            abort(409, "Member with this id already exists, please change its id")
        register[Register_id] = {'name' : request.json['name'], 'lname' : request.json['lname']}
        return redirect("/RegisterList")
    
    def put(self, Register_id):
        if Register_id in register:
            print("Member with this id does not exists, please give proper id")
        register[Register_id] = {'name' : request.json['name'], 'lname' : request.json['lname']}
        return redirect("/RegisterList")

    def delete(self, Register_id):
        if Register_id in register:
            print("Member with this id does not exists, please give proper id")
        del register[Register_id]
        return redirect("/RegisterList")









class GetDataFromModel(Resource):
    def get(self):
        try:
            data = register.query.all()
            for i in data:
                print(i)
            return [register.serialize(record) for record in data]
        except Exception as e:
            df = {
                "Error" : "Something went Worng in get",
                "Error_Message" : e
            }
            print("Error :" , e)
            return df
        



api.add_resource(HelloWorld,"/")
api.add_resource(HelloName,"/<string:name>")
api.add_resource(RegisterList,"/RegisterList")
api.add_resource(Register,"/Register/<int:Register_id>")
api.add_resource(GetDataFromModel, "/GetDataFromModel/all")


if __name__ == '__main__':
    app.run(debug=True)

