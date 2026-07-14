from datetime import timedelta
from functools import wraps
from flask import Flask, flash, render_template, redirect, session, url_for,request
from werkzeug.security import generate_password_hash, check_password_hash

import logging
import sqlite3
import logout

DATABASE = 'users.db'

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
app.permanent_session_lifetime = timedelta(hours=1)  # Set session lifetime to 1 hour (3600 seconds)
 # Set a secret key for session management and flash messages
app.secret_key = "TheMasterSeries1234"


def get_db_connection():
    """Return a SQLite connection. Raised errors propagate to the caller."""
    return sqlite3.connect(DATABASE)
# returning a string variable in the URL
@app.route('/', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout_route():
    return logout.logout_user()  # Call the logout function from the logout module

# @app.route('/home/<name>')
# def hello(name):
#     return f'Hello, {name}!'

# Decorator to check if the user is logged in and is an admin
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in') or session.get('user_type') != 'admin':
            flash("Unauthorized access. Please log in as an admin.", "error")
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return wrapper

def user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in') or session.get('user_type') != 'user':
            flash("Unauthorized access. Please log in as a user.", "error")
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return wrapper

# Admin route that requires the user to be logged in as an admin with the admin_required decorator
@app.route('/admin')
@admin_required
def admin():
    if 'user_id' in session and session.get('user_type') == 'admin':
        return render_template('admin.html', admin_name=session.get('username'))

    return redirect(url_for('login_page'))

@app.route('/user')
@user_required
def user():
    return render_template('user.html', guest_name=session.get('username'))


# Initialize the SQLite database and create the users table if it doesn't exist
def init_db():
    connectObj = None
    try:
        connectObj = get_db_connection()
        cursorObj = connectObj.cursor()
        cursorObj.execute('''
            CREATE TABLE IF NOT EXISTS LoginDetails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT  NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            )
        ''')
        connectObj.commit()
    except sqlite3.Error:
        app.logger.exception("Failed to initialize the database")
        raise
    finally:
        if connectObj is not None:
            connectObj.close()

    # call the function to initialize the database when the application starts
init_db()


#Register user
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        user_type = request.form.get('user')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([email, username, user_type, password, confirm_password]):
            flash("All fields are required.", "error")
            return redirect(url_for('register_user'))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('register_user'))

        # Store the hashed password in the database
        connectObj = None
        try:
            connectObj = get_db_connection()
            cursorObj = connectObj.cursor()

            cursorObj.execute('SELECT * FROM LoginDetails WHERE email = ?', (email,))
            existing_user = cursorObj.fetchone()

            # Check if the user already exists based on email
            if existing_user:
                flash("User already exists. Please choose a different username or email.", "error")
                return redirect(url_for('register_user'))

            actual_password = generate_password_hash(password)
            cursorObj.execute('INSERT INTO LoginDetails (email, username, password, user_type) VALUES (?, ?, ?, ?)',
                                (email, username, actual_password, user_type))
            connectObj.commit()
        except sqlite3.Error:
            app.logger.exception("Failed to register user")
            flash("Registration failed due to a server error. Please try again.", "error")
            return redirect(url_for('register_user'))
        finally:
            if connectObj is not None:
                connectObj.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login_page'))

    # For GET request, render the registration form
    return render_template('register.html')


#password validation and redirection based on user type
@app.route('/validate_login', methods=['POST'])
def validate_login():                    
    username = request.form.get('username')
    user_type = request.form.get('user')
    user_password = request.form.get('password')

    if not all([username, user_type, user_password]):
        flash("All fields are required.", "error")
        return redirect(url_for('login_page'))

    #fetchout user password from LoginDetails Table and compare the password with the hashed password in the database
    connectObj = None
    try:
        connectObj = get_db_connection()
        cursorObj = connectObj.cursor()

        cursorObj.execute('SELECT id,password FROM LoginDetails WHERE username = ? AND user_type = ?',
                           (username, user_type))
        result = cursorObj.fetchone()
    except sqlite3.Error:
        app.logger.exception("Failed to validate login")
        flash("Login failed due to a server error. Please try again.", "error")
        return redirect(url_for('login_page'))
    finally:
        if connectObj is not None:
            connectObj.close()

    if result:
        user_id,stored_password = result
        if stored_password and check_password_hash(stored_password, user_password):

            session['user_id'] = user_id
            session['username'] = username
            session['user_type'] = user_type
            session['logged_in'] = True
            session.permanent = True  # Make the session permanent (optional)

            return redirect(url_for('admin' if user_type == 'admin' else 'user'))

    flash("Invalid credentials. Please try again.", "error")
    return redirect(url_for('login_page'))




# app.add_url_rule('/home', 'home', hello)

# returning html page with the render_template function
# @app.route('/')
# def index_page():
#     return render_template('index.html')



@app.route('/blog/<int:post_id>')
def blog_page(post_id):
    return f'This is blog post number {post_id}.'


@app.errorhandler(404)
def not_found_error(error):
    return render_template('login.html'), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.exception("Internal server error")
    flash("An unexpected error occurred. Please try again later.", "error")
    return render_template('login.html'), 500

# @app.route('/login/<username>', methods=['POST'])
# def login(username):
#     # Handle login logic here
    
#     password = request.form['password']
#     # Validate credentials and perform login
#     if request.method == 'POST':
#         username = request.form['username']
#         return redirect(url_for('index_page', username=username))
#         # Process login form data
#     else:
#         username = request.args.get('username')
#         return redirect(url_for('user', guest_name=username))
          

if __name__ == '__main__':
    app.run(debug=True)