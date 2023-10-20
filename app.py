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
            return render_template('home_page.html', current_user=username)
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
        database.create_collection(str(username)+'_calendar') 
        return "Registration Successful"
    else:
        return "Registration Failed (Username already in use)"

@app.route('/home/<parameter>')
def home(parameter):
    return render_template('home_page.html', current_user = parameter)

@app.route('/entries/<parameter>')
def entries(parameter):
    return render_template('entries.html',current_user = parameter)

@app.route('/calendar/<parameter>')
def calendar(parameter):
    dates = []
    cursor = database[str(parameter) + '_calendar'].find({}, {"date": 1, "_id": 0})
    for doc in cursor:
        dates.append(doc["date"])
    return render_template('calendar.html', current_user = parameter, checked_dates=dates)

@app.route('/checkin/<parameter>', methods=["GET", "POST"])
def checkin(parameter):
    if request.method == "POST":
        if not database[str(parameter)+'_calendar'].find_one({'date': request.form["date"]}):
            database[str(parameter)+'_calendar'].insert_one({"date": request.form["date"]})
    dates = []
    cursor = database[str(parameter) + '_calendar'].find({}, {"date": 1, "_id": 0})
    for doc in cursor:
        dates.append(doc["date"])
    return render_template("calendar.html", current_user = parameter, checked_dates=dates)

@app.route('/account/<parameter>')
def account(parameter):
    #not done
    return render_template('account.html')

if __name__ == '__main__':
    app.run()
