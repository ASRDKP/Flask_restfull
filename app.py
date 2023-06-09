from flask import Flask, redirect, request, jsonify
from flask_restful import Api, Resource,reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import json
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)



app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root1234@localhost:3306/newhospitaldb'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)




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



class registerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = register
        
    id = ma.auto_field()
    name = ma.auto_field()
    lname = ma.auto_field()








class RegisterModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    
# db.create_all()

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
        


class GetDataFromModelbyID(Resource):
    def get(self,Register_id):
        try :
            filter = register.query.filter_by(id=Register_id)
            desc = 'Record with id={} is not available'.format(Register_id)
            return register.serialize(filter.first_or_404(description = desc))
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromModelbyID.get",
                "Error_Message" : e
            }
            print("Error :" , e)
            return df
    
   
    def post(self, Register_id):
        try:
            print("Data", request.json)
            udata = register(id = Register_id, name = request.json['name'], lname = request.json['lname'])
            db.session.add(udata)
            db.session.commit()
            return register.serialize(register.query.filter_by(id=Register_id).first_or_404(description='Record with id={} is not available'.format(Register_id)))
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromModelbyID.POST ",
                "Error_Message" : e.args[0]
            }
            print("Error :" , e)
            return df

    
    def put(self, Register_id):
        try:
            udata = register.query.get_or_404(Register_id)
            if udata is None:
                return ("No Data With the given Register_id = {}. Please Enter valid Register_id").format(Register_id)
            udata.name = request.json['name']
            udata.lname = request.json['lname']
            db.session.commit()
            return "Id is Successfully Updated."
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromModelbyID.put",
                "Error_Message" : e
            }
            print("Error :" , e)
            return df
    
    
    def patch(self, Register_id):
        try:
            udata = register.query.get_or_404(Register_id)
            if udata is None:
                return ("No Data With the given Register_id = {}. Please Enter valid Register_id").format(Register_id)
            if 'name' in request.json:
                udata.name = request.json['name']
            if 'lname' in request.json:
                udata.lname = request.json['lname']
            db.session.commit()
            return "Id is Successfully Updated."
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromModelbyID.patch",
                "Error_Message" : e
            }
            print("Error :" , e)
            return df

    
    def delete(self, Register_id):
        try :
            udata = register.query.get(Register_id)
            if udata is None:
                return ("No Data With the given Register_id = {}. Please Enter valid Register_id").format(Register_id)
            db.session.delete(udata)
            db.session.commit()
            return "Deleted Successfully."
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromModelbyID.delete",
                "Error_Message" : e
            }
            print("Error :" , e)
            return df



class GetDataFromSchema(Resource):
    def get(self):
        try:
            data = register.query.all()
            print(data)
            registers_schema = registerSchema(many=True)
            udata = registers_schema.dumps(data)
            print("UData :" , udata)
            print("Type :", type(udata))
            data = json.loads(udata)
            print("Type :", type(data))
            return data
            # return registers_schema.dumps(data)
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromSchema.getall",
                "Error_Message" : e
            }
            print("Error :" , e)
            return df


class GetDataFromSchemabyID(Resource):
    def get(self, Register_id):
        try:
            print("Register_id :" , Register_id)
            data = register.query.filter_by(id=Register_id)
            print("Daataa", data)
            registers_schema = registerSchema(many=True)
            udata = registers_schema.dumps(data)
            print("UData :" , udata)
            print("Type :", type(udata))
            data = json.loads(udata)
            print("Type :", type(data))
            return data
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromSchemabyID.getbyid",
                "Error_Message" : e
            }
            print("Error :" , e)
            return df   
           
    
    def post(self, Register_id):
        try:
            data = register(id = Register_id, name = request.json['name'], lname = request.json['lname'])
            print("Data :" , data)
            db.session.add(data)
            print("$$#%$$#$$")
            db.session.commit()
            print("$$#%$$#$$")
            registers_schema = registerSchema()
            registers_schema.dumps(data)
            return redirect("/GetDataFromSchema/all")
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromSchemabyID.getbyid",
                "Error_Message" : e.args[0]
            }
            print("Error :" , e.args[0])
            return df 
        
        
        
    def put(self, Register_id):
        try:
            data = register.query.get_or_404(Register_id)
            print("Data",data)
            print("Type of Data",type(data))
            if data is None:
                message = "Data with the given Id does not exist."
                print(message)
                return message
            data.name = request.json['name']
            data.lname = request.json['lname']
            db.session.commit()
            registers_schema = registerSchema()
            registers_schema.dumps(data)
            # return redirect("/GetDataFromSchema/all")
            return "Data Updated"
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromSchemabyID.put",
                "Error_Message" : e
            }
            print("Either The Id is invalid or Something went wrong ")
            print("Error :" , e)
            return df    

    
    def delete(self, Register_id):
        try:
            data = register.query.get(Register_id)
            if data is None:
                return ("No Data With the given Register_id = {}. Please Enter valid Register_id").format(Register_id)
            db.session.delete(data)
            db.session.commit()
            registers_schema = registerSchema()
            registers_schema.dumps(data)
            return "Deleted Successfully."
        except Exception as e:
            df = {
                "Error" : "Something went Worng in GetDataFromSchemabyID.put",
                "Error_Message" : e
            }
            print("Either The Id is invalid or Something went wrong ")
            print("Error :" , e)
            return df   
        
api.add_resource(HelloWorld,"/")
api.add_resource(HelloName,"/<string:name>")
api.add_resource(RegisterList,"/RegisterList")
api.add_resource(Register,"/Register/<int:Register_id>")
api.add_resource(GetDataFromModel, "/GetDataFromModel/all")
api.add_resource(GetDataFromModelbyID, "/GetDataFromModelbyID/<int:Register_id>")
api.add_resource(GetDataFromSchema, "/GetDataFromSchema/all")
api.add_resource(GetDataFromSchemabyID, "/GetDataFromSchemabyID/<int:Register_id>")

if __name__ == '__main__':
    app.run(debug=True)

