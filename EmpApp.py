from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql import connections
import os
import pymysql
from config import *

app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route('/')
def Index():
    conn = db_conn
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM employee')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html', employee = data)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    conn = db_conn
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        id = request.form['id']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']
        gender = request.form['gender']
        salary = request.form['salary']
        cur.execute("INSERT INTO employee (id, firstName, lastName, email, contact, address, gender, salary) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (id, firstName, lastName, email, contact, address, gender, salary))
        conn.commit()
        flash('Employee Added Successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    conn = db_conn
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM employee WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', employee = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_employee(id):
    conn = db_conn
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']
        gender = request.form['gender']
        salary = request.form['salary']

        cur.execute("""
            UPDATE employee
            SET firstName = %s,
                lastName = %s,
                email = %s,
                contact = %s,
                address = %s,
                gender = %s,
                salary = %s
            WHERE id = %s
        """, (firstName, lastName, email, contact, address, gender, salary, id))
        flash('Employee Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    conn = db_conn
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM employee WHERE id = {0}'.format(id))
    conn.commit()
    flash('Employee Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
