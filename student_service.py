import sqlite3
from flask import flash, render_template, request
import os
print("DB PATH:", os.path.abspath('users.db'))


def dashboard_page():
    return render_template('dashboard.html')

def create_students_table():
    connectObj = sqlite3.connect('users.db')
    cursorObj = connectObj.cursor()
    cursorObj.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            dob DATE,
            gender TEXT,
            grade INTEGER,
            address TEXT,
            enrollment_date DATE,
            parent_name TEXT,
            roll_number TEXT UNIQUE NOT NULL 
        )
    ''')
    connectObj.commit()
    connectObj.close()

create_students_table()  # Call the function to create the Students table when the application starts   

def add_student():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        gender = request.form['gender']
        grade = request.form['grade']
        address = request.form['address']
        enrollment_date = request.form['enrollment_date']
        parent_name = request.form['parent_name']
        # Insert data into the database
        connectObj = sqlite3.connect('users.db')
        cursorObj = connectObj.cursor()

        roll_number = generate_roll_number()
        cursorObj.execute('INSERT INTO Students ( roll_number,first_name, last_name, email, phone, dob, gender, grade, address, enrollment_date, parent_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (roll_number, first_name, last_name, email, phone, dob, gender, grade, address, enrollment_date, parent_name))
        
        connectObj.commit()
        connectObj.close()
        
        flash("You added a new student successfully!", "success")
        # return student_service.dashboard_page()  # Redirect to the dashboard after adding a student
    
    # For GET request, render the add student form
    return render_template('add_student.html')



# def add_student():
#     return render_template('add_student.html')

def view_student_data():
    
    # if request.method == 'POST':
            # search_query = request.form['search']
            connObj = sqlite3.connect('users.db')
            cursorObj = connObj.cursor()
            cursorObj.execute("SELECT * FROM Students")
            students = []
            rows = cursorObj.fetchall()
            for row in rows:
                student = {
                    'id': row[0],
                    'roll_number': row[11],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'dob': row[5],
                    'gender': row[6],
                    'grade': row[7],
                    'address': row[8],
                    'enrollment_date': row[9],
                    'parent_name': row[10]
                }

                students.append(student)
                 
            cursorObj.close()
            connObj.close()
         
            return render_template('view_student.html', students=students)

# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()

# cursor.execute("SELECT * FROM Students")
# print(cursor.fetchall())
          # routers.view_student_data()  # Redirect to the view student data page after fetching the data
    
    # Pass the students data to the template for rendering using http request method GET 
    
def generate_roll_number():
    connObj = sqlite3.connect('users.db')
    cursorObj = connObj.cursor()
    cursorObj.execute("SELECT roll_number FROM Students order by id DESC LIMIT 1")
    max_roll_number = cursorObj.fetchone()
    if max_roll_number and max_roll_number[0]:
        max_roll_number = int(max_roll_number[0].split('ROLL')[1]) 
        new_roll_number = max_roll_number + 1  # Extract the numeric part of the roll number
    else:
        new_roll_number = 1
    roll_number = f"ROLL{new_roll_number:04d}"
    connObj.close()
    return roll_number