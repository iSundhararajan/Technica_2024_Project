from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from datetime import datetime
import os.path
from propelauth_flask import init_auth, current_user

# create the app
app = Flask(__name__)
db_name = 'IntegriMed.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create database tables
class StoringHashes(db.Model):
    __tablename__ = 'storing_hashes'
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.LargeBinary, nullable=False)
    expirydate = db.Column(db.DateTime, nullable=False)

class StoringFiles(db.Model):
    __tablename__ = 'storing_files'
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(200), nullable=False)
    hashid = db.Column(db.Integer, db.ForeignKey("storing_hashes.id"))
    sentid = db.Column(db.Integer, db.ForeignKey("users.id"))
    receivedid = db.Column(db.Integer, db.ForeignKey("users.id"))

class User(db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    affiliatedHospital = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    userType = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        fullName = self.firstName + " " + self.lastName
        return '<Name %r, email %r, affiliatedHospital %r, User Type %r>' % (fullName, self.email, self.affiliatedHospital, self.userType)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_password', methods=['POST','GET'])
def find_users_password():
    try:
        stmt = text("SELECT password FROM users WHERE email = :x")
        email_input = request.form.get('email')
        stmt = stmt.bindparams(x=email_input)
        password = db.session.execute(stmt).fetchone()
        if password and password[0] == request.form.get('password'):
            return render_template('account.html')
        else:
            return "Incorrect password or email not found"
    except Exception as e:
        return f"There is an error: {e}"

@app.route('/signup', methods=['POST', 'GET'])
def account():
    title = "Account"
    if request.method == "POST":
        userName = request.form.get('Name', '')
        emailI = request.form.get('Email')
        affiliatedHospitalI = request.form.get('Affiliated Hospital')
        passwordI = request.form.get('Password')
        userTypeI = request.form.get('UserType')
        
        name_parts = userName.split(" ", 1)
        firstNameI = name_parts[0]
        lastNameI = name_parts[1] if len(name_parts) > 1 else ""

        if not (emailI and affiliatedHospitalI and passwordI and userTypeI):
            return "All fields are required", 400  # 400 Bad Request if any field is missing

        newUser = User(
            firstName=firstNameI,
            lastName=lastNameI,
            email=emailI,
            affiliatedHospital=affiliatedHospitalI,
            password=passwordI,
            userType=userTypeI
        )
        try:
            db.session.add(newUser)
            db.session.commit()
            return render_template('account.html', title="Account", user=User)
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  
            return "There was an error adding your Account", 500  # 500 Internal Server Error
    else:
        return render_template('signup.html', title="SignUp", user=User)

'''
@app.route('/registration', methods=['POST', 'GET'])
def account():
    title = "Account"
    if request.method == "POST":
        userName = request.form['Name']
        firstNameI, lastNameI = userName.split(" ")
        newUser = User(
            firstName=firstNameI,
            lastName=lastNameI,
            email=request.form['Email'],
            affiliatedHospital=request.form['Affiliated Hospital'],
            password=request.form['Password'],
            userType=request.form['UserType']
        )
        try:
            db.session.add(newUser)
            db.session.commit()
            return redirect('/madeAccount')
        except:
            db.session.rollback()
            return "There was an error adding your Account"
    else:
        return render_template('registration.html', title="Registration", user=User)

@app.route('/madeAccount')
def made_account():
    return "Account created successfully!"
'''
''' - This would be the code for updating an account  will not implement this functionality for now 
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    userToUpdate = User.query.get_or_404(id)
    if request.method == "POST":
        firstNameI, lastNameI = request.form['Name'].split(" ")
        userToUpdate.firstName = firstNameI
        userToUpdate.lastName = lastNameI
        try:
            db.session.commit()
            return redirect('/account')
        except:
            db.session.rollback()
            return "There was a problem updating that user"
    else:
        return render_template('update.html', userToUpdate=userToUpdate)
'''
@app.route('/delete/<int:id>')
def deleteUser(id):
    userToDelete = User.query.get_or_404(id)
    try:
        db.session.delete(userToDelete)
        db.session.commit()
        return redirect('/account')
    except:
        db.session.rollback()
        return "There was a problem deleting that user"

def delete_hash_and_file(hashID, fileID):
    hash = StoringHashes.query.get(hashID)
    file = StoringFiles.query.get(fileID)
    date = datetime.now()

    if (hash and file) and date >= hash.expirydate:
        try:
            db.session.delete(hash)
            db.session.delete(file)
            db.session.commit()
            print(f"Hash and file with ID {hashID} and {fileID} deleted")
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
    else:
        print("Hash or file could not be deleted as they don't exist or are not expired")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)