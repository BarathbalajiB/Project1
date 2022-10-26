from flask import Flask, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Flask'
app.config['MONGO_URI'] = "mongodb+srv://moo1-student:m001-mongodb-basics@sandbox.pmgteep.mongodb.net/?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as the following user:' + session['username']
    
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['passworrd'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return 'Invalid username or password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.methods == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    
        return 'Username already exist in database'
    return render_template('register.html')

if __name__ == "__main__":
    app.secret_key= 'secretivekeyagain'
    app.run(debug = True) 

