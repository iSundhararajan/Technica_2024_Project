from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import hashlib


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.db'

# Initilising the database

db = SQLAlchemy(app)

#Create database tables

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



@app.route('/')
def index():
    return render_template('index.html')
    
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
        return jsonify("Generating hash...")
        
def generate_hash(f):
    hasher = hashlib.sha256()

    for chunk in iter(lambda: f.read(4096), b""):
        hasher.update(chunk)

    print('{}: {}'.format(hasher.name, hasher.hexdigest()))
    return hasher.hexdigest()


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True) 