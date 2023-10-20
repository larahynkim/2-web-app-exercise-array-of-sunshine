from flask import Flask, render_template, request, redirect, url_for 
from pymongo import MongoClient 

app = Flask(__name__)
client = MongoClient('localhost', 27017) 
database = client.get_database('mindscape')  
users = database.get_collection('users') 



@app.route('/')
def start():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists in the database
    user = users.find_one({'username': username})

    if user:
        # Check if the provided password matches the stored hashed password
        if password == user['password']:
            return render_template('home_page.html')
        else:
            return "Login Failed (Invalid Password)"
    else:
        return "Login Failed (User not found)"


@app.route('/register', methods=['POST'])
def register():
    return render_template('create_new_account.html')

@app.route('/createNewAccount', methods=['POST'])
def create_new_account():
    username = request.form['username']
    password = request.form['password']

    # Check if the username is already in use
    if not users.find_one({'username': username}):
        user_data = {
            'username': username,
            'password': password
        }
        users.insert_one(user_data)
        return "Registration Successful"
    else:
        return "Registration Failed (Username already in use)"

@app.route('/home')
def home():
    return render_template('home_page.html')

@app.route('/entries')
def entries():
    return render_template('entries.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/account')
def account():
    return render_template('account.html')

if __name__ == '__main__':
    app.run()
