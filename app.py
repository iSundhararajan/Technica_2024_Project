from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLALchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.db'

# Initilising the database

db = SQLALchemy(app)

#Create database tables

#Make two separate tables for doctors and patitents
class User(db.model):
    id = db.column(db.Integer, primary_key = True)
    firstName = db.Column(db.string(200), nullable=False)
    lastName = db.Column(db.string(200), nullable=False)
    email = db.Column(db.string(200), nullable=False)
    password =  db.Column(db.string(200), nullable=False)

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



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)