from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'intellipaat'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/intellipaat'
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name': request.form['username']})

        if login_user:
            hashed_password = login_user['password']
            provided_password = request.form['pass'].encode('utf-8')

            if bcrypt.checkpw(provided_password, hashed_password):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        return 'Invalid username or password combination'
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'Username already in database'
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)
