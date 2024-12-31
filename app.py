from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration for MongoDB
app.config.from_object('config.Config')

# Initialize PyMongo
mongo = PyMongo(app)

# Set up secret key for session management
app.secret_key = os.urandom(24)

# Routes for signup, login, and home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')

        # Check if user exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('signup'))

        # Insert user into MongoDB
        mongo.db.users.insert_one({
            'username': username,
            'password': hashed_password
        })

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check user credentials
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            session['username'] = username  # Store the username in the session
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Ensure the user is logged in
    if 'username' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

    username = session['username']  # Get the username from session
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    # Add logout logic here (e.g., clear session or cookies)
    return redirect(url_for('index'))




@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
