from flask import Flask, render_template, request, redirect, url_for 
from pymongo import MongoClient 
import requests
import random 
from bson import ObjectId
import certifi
from flask_cors import CORS
from flask import json


ca = certifi.where()
ATLAS_URI = 'mongodb+srv://admin:admin@cluster0.lulecqi.mongodb.net/?retryWrites=true&w=majority'
app = Flask(__name__)
client = MongoClient(ATLAS_URI) 
client = MongoClient(ATLAS_URI, tlsCAFile=ca)
database = client.get_database('mindscape')  
users = database.get_collection('users') 
client = MongoClient(ATLAS_URI, tlsAllowInvalidCertificates=True)
app = Flask(__name__)
CORS(app)

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
             return redirect(url_for('home', parameter=username))
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
        return redirect(url_for('start'))
    else:
        return "Registration Failed (Username already in use)"
    

def get_daily_affirmation():
    response = requests.get('https://zenquotes.io/api/today')
    if response.status_code == 200:
        return response.json()[0]['q']
    return None

def get_daily_challenges(n=3):
    challenges = [
        "Take 5 minutes to meditate.",
        "Write down three things you're grateful for.",
        "Listen to calming music for 10 minutes.",
        "Take a short walk outside and focus on your surroundings.",
        "Speak to a loved one or friend.",
        "Avoid screen time for an hour before bed.",
        "Read a book for 15 minutes.",
        "Try out a new hobby.",
        "Do 5 minutes of deep breathing.",     
        "Drink more water.",   
        "Take your vitamins.",   
        "Sleep for 8-9 hours every night.",   
        "Take a 30 minute walk.",   
        "Go to the gym.",   
        "No complaining.",   
        "No cursing.",   
        "No fast food.",   
        "Pay someone a compliment.",   
        "Read 20 pages of a book.",   
        "Write down three things you're grateful for.",
        "Take a 15-minute walk outside and focus on your surroundings.",
        "Reach out to a friend or family member you haven't spoken to in a while.",
        "Try a new recipe or cook a meal from scratch.",
        "Take 5 minutes to meditate and focus on your breathing.",
        "Declutter and organize a small area of your home or workspace.",
        "Read for at least 20 minutes from a book you enjoy.",
        "Write a positive affirmation and repeat it to yourself throughout the day.",
        "Try a new hobby or activity you've been interested in.",
        "Perform a random act of kindness for someone.", 
        "Start your day with a healthy breakfast and mindful eating.",
		"Take a break every hour during work or study to stretch or move around.",
		"List five things you've accomplished recently, no matter how small.",
		"Practice deep breathing for five minutes in a quiet space.",
		"Challenge yourself to learn a new word and use it in a sentence.",
		"Compliment someone genuinely.",
		"Spend 10 minutes tidying up your living or work space.",
		"Identify and write down one personal or professional goal for the month.",
		"Go to bed 30 minutes earlier than usual to ensure you get enough rest.",
		"Take a moment to appreciate a piece of art, whether it’s in a museum, online, or on the street."
    ]
    return random.sample(challenges, n)

@app.route('/home/<parameter>')
def home(parameter):
    daily_affirmation = get_daily_affirmation()
    daily_challenges = get_daily_challenges()
    return render_template('home_page.html', current_user = parameter, daily_affirmation=daily_affirmation, daily_challenges=daily_challenges)

# @app.route('/entries/<parameter>')
# def entries(parameter):
#     return render_template('entries.html',current_user = parameter)

@app.route('/calendar/<parameter>')
def calendar(parameter):
    dates = []
    cursor = database[str(parameter) + '_calendar'].find({}, {"date": 1, "_id": 0})
    for doc in cursor:
        dates.append(doc["date"])
    return render_template('calendar.html', current_user=parameter, checked_dates=dates)

@app.route('/checkin/<parameter>', methods=["GET", "POST"])
def checkin(parameter):
    if request.method == "POST":
        if not database[str(parameter)+'_calendar'].find_one({'date': request.form["date"]}):
            database[str(parameter)+'_calendar'].insert_one({"date": request.form["date"]})
    dates = []
    cursor = database[str(parameter) + '_calendar'].find({}, {"date": 1, "_id": 0})
    for doc in cursor:
        dates.append(doc["date"])
    return render_template("calendar.html", current_user=parameter, checked_dates=dates)

@app.route('/account/<parameter>')
def account(parameter):
    #not done
    return render_template('account.html', current_user=parameter)

@app.route('/logout')
def logout():
    return redirect(url_for('start'))

#add an entry 
@app.route('/add_entry/<username>', methods=['POST'])
def add_entry(username):
    content = request.form['journal_entry']
    entries_collection = database.get_collection(str(username) + '_entries')
    entries_collection.insert_one({"content": content})
    return redirect(url_for('entries', parameter=username))

#get all entries
@app.route('/entries/<parameter>')
def entries(parameter):
    entries_collection = database.get_collection(str(parameter) + '_entries')
    all_entries = list(entries_collection.find())
    return render_template('entries.html', current_user=parameter, entries=all_entries)

# #edit an entry
@app.route('/edit_entry/<username>/<entry_id>')
def edit_entry(username, entry_id):
    entries_collection = database.get_collection(str(username) + '_entries')
    entry = entries_collection.find_one({"_id": ObjectId(entry_id)})
    if entry:
        return render_template('edit_entry.html', current_user=username, entry_id=entry_id, current_entry_content=entry['content'])
    else:
        return "Entry not found", 404

#handle form submission 
@app.route('/save_edit/<username>/<entry_id>', methods=['POST'])
def save_edit(username, entry_id):
    updated_content = request.form['journal_entry']
    entries_collection = database.get_collection(str(username) + '_entries')
    entries_collection.update_one({"_id": ObjectId(entry_id)}, {"$set": {"content": updated_content}})
    return redirect(url_for('entries', parameter=username))


#delete an entry 
@app.route('/delete_entry/<username>/<entry_id>')
def delete_entry(username, entry_id):
    entries_collection = database.get_collection(str(username) + '_entries')
    entries_collection.delete_one({"_id": ObjectId(entry_id)})
    return redirect(url_for('entries', parameter=username))

@app.route('/search_entries/<username>', methods=['POST'])
def search_entries(username):
    search_query = request.form['search_query']
    entries_collection = database.get_collection(str(username) + '_entries')
    search_results = list(entries_collection.find({"content": {"$regex": search_query, "$options": "i"}}))
    all_entries = list(entries_collection.find())
    return render_template('entries.html', current_user=username, entries=all_entries, search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)