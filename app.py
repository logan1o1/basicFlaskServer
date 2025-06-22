from flask import Flask, render_template, request, url_for, redirect, flash
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_bcrypt import Bcrypt
import os, re

app = Flask(__name__, template_folder= "templates")
app.config.from_object('config.Config')

mongo_uri = "mongodb+srv://saswatm2706:dHjmAXPB73AgFsVW@cluster0.uynsq0f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri, server_api = ServerApi('1'))
db = client['test_db']
users_collection = db['users']

bcrypt = Bcrypt(app)

def inValid(email):
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
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if users_collection.find_one({'username':username}):
            flash("Username already exists, choose a diff one", "warning")
            return
        else:
            users_collection.insert_one({
                'username':username,
                'email': email,
                'password': hashedPassword
            })        
            flash("Registration was successfull, you can now login", "success")
            return redirect(url_for("login"))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username':username})
        if user:
            is_valid = bcrypt.check_password_hash(user.password, password)
            if is_valid:
                flash("Login successful", "success")
            else:
                flash("Invalid Password", "danger")
        else:
            flash("User not found", "warning")
        
    return render_template('login.html')


try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)