from datetime import timedelta
from functools import wraps
from flask import Flask, abort, flash, render_template, redirect, session, url_for,request
from werkzeug.security import generate_password_hash, check_password_hash
import student_service

import sqlite3
import logout

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=1)  # Set session lifetime to 1 hour (3600 seconds)
 # Set a secret key for session management and flash messages
app.secret_key = "TheMasterSeries1234" 
# returning a string variable in the URL
@app.route('/', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')

# Route for logging out the user
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
            abort(403)
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
    
    return render_template('/')    

@app.route('/user')
@user_required
def user():
    if 'user_id' in session and session.get('user_type') == 'user':
        return render_template('user.html', guest_name=session.get('username'))
    
    return render_template('/')    


# Initialize the SQLite database and create the users table if it doesn't exist
def init_db():
    connectObj = sqlite3.connect('users.db')
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
    connectObj.close()

    # call the function to initialize the database when the application starts
init_db()






#Register user
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        user_type = request.form['user']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
             flash("Passwords do not match.", "error")
          
    # Store the hashed password in the database
        connectObj = sqlite3.connect('users.db')
        cursorObj = connectObj.cursor()

        cursorObj.execute('SELECT * FROM LoginDetails WHERE email = ?', (email,))
        existing_user = cursorObj.fetchone()

        # Check if the user already exists based on email
        if existing_user:
           
            flash("User already exists. Please choose a different username or email.", "error")
            connectObj.close()
            return redirect(url_for('register_user'))

        actual_password = generate_password_hash(password)
        cursorObj.execute('INSERT INTO LoginDetails (email, username, password, user_type) VALUES (?, ?, ?, ?)',
                            (email,username,actual_password, user_type))
        
        
        connectObj.commit()
        connectObj.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login_page'))

    # For GET request, render the registration form
    return render_template('register.html')

    
#password validation and redirection based on user type
@app.route('/validate_login', methods=['POST'])
def validate_login():                    
    username = request.form['username']
    user_type = request.form['user']
    user_password = request.form['password']

    #fetchout user password from LoginDetails Table and compare the password with the hashed password in the database
    connectObj = sqlite3.connect('users.db')
    cursorObj = connectObj.cursor()

    cursorObj.execute('SELECT id,password FROM LoginDetails WHERE username = ? AND user_type = ?',
                       (username, user_type))
    result = cursorObj.fetchone()
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
        
            # if user_type == 'admin':
            #     return redirect(url_for('admin', username=username))
            # elif user_type == 'user':
            #     return redirect(url_for('user', username=username))
    print(session) 
    flash("Invalid credentials. Please try again.", "error")
    return redirect(url_for('login_page'))

   


# app.add_url_rule('/home', 'home', hello)

# returning html page with the render_template function
# @app.route('/')
# def index_page():
#     return render_template('index.html')


@app.route('/dashboard')
@admin_required 
def dashboard():
    return student_service.dashboard_page() 

def create_stud_table():
    student_service.create_students_table()  # Call the create_students_table function from the student_service module to create the Students table in the database

@app.route('/add_student',methods=['POST','GET'])
@admin_required
def add_student_record():
    return student_service.add_student()  # Call the add_student function from the student_service module to handle adding a new student


# @app.route('/blog/<int:post_id>')
# def blog_page(post_id):
#     return f'This is blog post number {post_id}.'

# Call the student_data function from the view_student module to fetch and display student data
@app.route('/view_student' , methods=['GET', 'POST'])
@admin_required
def view_student():
    return student_service.view_student_data()  # Call the view_student_data function from the student_service module to fetch and display student data

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