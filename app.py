from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__, template_folder= "templates")

mongo_uri = "mongodb+srv://saswatm2706:dHjmAXPB73AgFsVW@cluster0.uynsq0f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri, server_api = ServerApi('1'))
#dHjmAXPB73AgFsVW

@app.route("/")
def home():
    return render_template('index.html')

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)