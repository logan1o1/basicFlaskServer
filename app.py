from flask import Flask, render_template, request, url_for, redirect, flash
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os, re

app = Flask(__name__, template_folder= "templates")

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


cors = CORS(app)

mongo_uri = "mongodb+srv://saswatm2706:dHjmAXPB73AgFsVW@cluster0.uynsq0f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri, server_api = ServerApi('1'))
db = client['test_db']
users_collection = db['users']

bcrypt = Bcrypt(app)

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False


@app.route("/")
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash("post req")
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # is_valid_email = isValid(email)

        # if not is_valid_email:
        #     flash("The email is not in the correct format")

        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if users_collection.find_one({'username':username}):
            flash("Username already exists, choose a diff one", "warning")
            return render_template('register.html')
        else:
            users_collection.insert_one({
                'username':username,
                'email': email,
                'password': hashedPassword
            })        
            flash("Registration was successfull, you can now login", "success")
            return redirect(url_for("login"))
    #return jsonify(users, status=200, mimetype='application/json'
    return render_template('register.html')


@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username':username})
        if user:
            is_valid = bcrypt.check_password_hash(user["password"], password)
            if is_valid:
                flash("Login successful", "success")
                return render_template('index.html')
            else:
                flash("Invalid Password", "danger")
                return render_template('login.html')
        else:
            flash("User not found", "warning")
            return render_template('login.html')
    return render_template('login.html')


try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

if __name__ == '__main__':
    app.run(debug=True)