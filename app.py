from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import hashlib


app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:////Users/brittany/Desktop/inspirigirl/Technica_2024_Project/users.db'
# /Users/brittany/Desktop/inspirigirl/Technica_2024_Project/app.py

# Initilising the database

db = SQLAlchemy(app)

#Create database tables


@app.route('/')
def index():
    return render_template('index.html')

class Hashes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(100), nullable=False)
    hashVal = db.Column(db.String(70), nullable=False)
    def __repr__(self):
        return '<File %r>' % self.id

@app.route('/add_hash', methods=['POST'])
def add_hash(f,hash):
    data = request.json
    # file_name = data['fileName']
    new_hash = Hashes(fileName=data['f'], hashVal=data["hash"])
    db.session.add(new_hash)
    db.session.commit()
    return jsonify({'message': 'Hash added!'}), 201

#Make two separate tables for doctors and patients
class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False) 
    lastName = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    #Create a function to return a string when add something
    #Use this function for when needing to show info on profile page name and whether patient or not
    def __repr__(self):
        return '<Name %r>' % self.id
    
    
@app.route('/account', methods = ['POST', 'GET'])
def account ():
    title = "Account"
    if request.method == "POST":
        userFirstName = request.form['name']
        newUser = User(name = userFirstName)

        #Push to Database

        try:
            db.session.add(newUser)
            db.session.commit()
            return redirect ('/madeAccount')
        except:
            return "There was an error adding your Account"
    else:
        return render_template('account.html')


@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file: 
        file_hash = generate_hash(file)
        search_response = search(file_hash)
        return jsonify(search_response)
        # return jso
    

def search(hash):
    # query = request.args.get('query')

    if hash:
        results = Hashes.query.filter((Hashes.hashVal == str(hash))).all()
        
        if results:
            print("File is IntegriMED certified!"),200
            # return jsonify("File is IntegriMED certified!"), 400
        else:
            print("WARNING: This file might have been tampered with")
    else:
        return jsonify({'message': 'Query parameter is required'}), 400


def generate_hash(f):
    hasher = hashlib.sha256()

    for chunk in iter(lambda: f.read(4096), b""):
        hasher.update(chunk)
    

    print('{}: {}'.format(hasher.name, hasher.hexdigest()))
    hash = hasher.hexdigest()
    return hash
    # add_hash_to_db(f.filename, hash) 
    # return hasher.hexdigest()

def add_hash_to_db(file_name, hash_value):
    new_hash = Hashes(fileName=file_name, hashVal=hash_value)
    db.session.add(new_hash)
    db.session.commit()
    return jsonify({'message': 'Hash added!'}), 201


# Run the Flask app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True) 