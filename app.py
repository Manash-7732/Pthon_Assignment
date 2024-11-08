from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo

app = Flask(__name__)

app.secret_key = "123456"
app.config['MONGO_URI'] = "mongodb+srv://Manash_7732:zCVeBidWmpxjaS67@cluster0.ooomc.mongodb.net/Assign"

try:
    mongo = PyMongo(app)
    print("Connected to MongoDB")
except pymongo.errors.ConnectionFailure as error:
    print("Could not connect to MongoDB:", error)

@app.route("/add", methods=['POST'])  
def add_user():
    _json = request.json
    _name = _json['name'] 
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password:
        _hashed_password = generate_password_hash(_password)
        try:
            result = mongo.db.Assign.insert_one({'name': _name, 'email': _email, 'password': _hashed_password})
            if result.inserted_id:
                resp = jsonify(message="User created successfully")
                resp.status_code = 200
                return resp
        except Exception as e:
            print("Error inserting document:", e)
            return jsonify(message="Failed to create user"), 500
    else:
        return not_found()
    
@app.route('/users')
def users():
    users=mongo.db.Assign.find();
    resp = dumps(users);
    return resp

@app.route("/users/<id>")
def user(id):
    user = mongo.db.Assign.find_one({'_id': ObjectId(id)});
    resp = dumps(user)
    return resp
@app.route("/delete/<id>" , methods = ['DELETE'])
def delete_user(id):
    mongo.db.Assign.delete_one({"_id":ObjectId(id)})
    respq = jsonify("user deleted successfully")

    respq.status_code = 200;
    return respq

@app.route("/update/<id>" , methods=["PUT"])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name'] 
    _email = _json['email']
    _password = _json['password']
    
    if _name and _email and _password and id:
        _hashed_password = generate_password_hash(_password)

        result = mongo.db.Assign.update_one(
                {'_id': ObjectId(id)},
                {'$set': {
                    'name': _name,
                    'email': _email,
                    'password': _hashed_password
                }}
            )
        resp = jsonify("User updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(debug=True)
