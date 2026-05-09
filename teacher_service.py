import sqlite3

from flask import flash, redirect, render_template, request, url_for



def generate_employee_number():
    connObj = sqlite3.connect('users.db')
    cursorObj = connObj.cursor()
    cursorObj.execute("SELECT employee_id FROM Teachers order by teacher_id DESC LIMIT 1")
    max_employee_number = cursorObj.fetchone()
    if max_employee_number and max_employee_number[0]:
        max_employee_number = int(max_employee_number[0].split('Tch')[1]) 
        new_employee_number = max_employee_number + 1  # Extract the numeric part of the roll number
    else:
        new_employee_number = 1
    emp_number = f"Tch{new_employee_number:04d}"
    connObj.close()
    return emp_number

def create_teachers_table():
    connectObj = sqlite3.connect('users.db')
    cursorObj = connectObj.cursor()
    cursorObj.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            dob DATE NOT NULL,
            gender TEXT NOT NULL,
            subject TEXT NOT NULL
        )
    ''')
    connectObj.commit()
    connectObj.close()

create_teachers_table()

def add_teacher():
    if request.method == 'GET':
        return render_template('add_teacher.html')

        # Get personal information
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']

        # Get contact information
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        # state = request.form['state']
        # zipcode = request.form['zipcode']
        # street = request.form['street']

        # # Get Teaching information
        # qualifications = request.form['qualifications']
        # hiredate = request.form['hiredate']
        
        employee_id = generate_employee_number()

        # Insert data into the database
        connectObj = sqlite3.connect('users.db')
        cursorObj = connectObj.cursor()

        cursorObj.execute('''
            INSERT INTO Teachers (employee_id,first_name, last_name, dob, gender, email, phone,subject)
            VALUES (?, ?, ?, ?, ?, ?,?,?)
        ''', (employee_id,first_name, last_name, dob, gender, email, phone,subject))

        connectObj.commit()
        connectObj.close()
        flash("You added a new teacher successfully!", "success")
        return render_template('add_teacher.html') 

def get_all_teachers(cursor):
    cursor.execute("SELECT * FROM Teachers")
    return cursor.fetchall()
   
    
def view_teachers():
    connObj = sqlite3.connect('users.db')
    cursorObj = connObj.cursor()
    
    rows = get_all_teachers(cursorObj)

    teachers = []
    for row in rows:
        teacher = {
                    'teacher_id': row[0],
                    'employee_id': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'email': row[4],
                    'phone': row[5],
                    'dob': row[6],
                    'gender': row[7],
                    'subject': row[8]
                }

        teachers.append(teacher)
    connObj.close()
    connObj.close()
    return render_template('view_teachers.html', teachers=teachers)

def delete_teacher_data(id):
    connObj = sqlite3.connect('users.db')
    cursorObj = connObj.cursor()
    cursorObj.execute("DELETE FROM Teachers WHERE teacher_id=?", (id,))
    connObj.commit()
    connObj.close()
    flash("You deleted a teacher successfully!", "success")
    return redirect(url_for('view_teacher'))

def view_teacher_for_edit(id):
    connObj = sqlite3.connect('users.db')
    connObj.row_factory = sqlite3.Row
    cursorObj = connObj.cursor()
    if request.method=='GET':
        cursorObj.execute("SELECT * FROM Teachers WHERE teacher_id=?", (id,))
        teacher = cursorObj.fetchone()
        connObj.close()
        # flash("You edited a student record successfully!", "success")
        return render_template('edit_teacher.html', teacher=teacher)

    if request.method=='POST':
        teacher = {
                    'teacher_id': id,
                    'employee_id': request.form['employee_id'],
                    'first_name': request.form['first_name'],
                    'last_name': request.form['last_name'],
                    'email': request.form['email'],
                    'phone': request.form['phone'],
                    'dob': request.form['dob'],
                    'gender': request.form['gender'],
                    'subject': request.form['subject']
                    }
        
        cursorObj.execute('''
            UPDATE Teachers
            SET teacher_id = ?, employee_id = ?, first_name = ?, last_name = ?, email = ?, phone = ?, dob = ?, gender = ?, subject = ?
            WHERE teacher_id = ?
        ''', (teacher['teacher_id'], teacher['employee_id'], teacher['first_name'], teacher['last_name'], teacher['email'], teacher['phone'], teacher['dob'], teacher['gender'], teacher['subject'], id))
        connObj.commit()
        connObj.close()
        flash(f"You have edited {teacher['first_name']} {teacher['last_name']} record successfully!", "success")
        return redirect(url_for('view_teacher'))
        # state = request.form['state']
        # zipcode = request.form['zipcode']
