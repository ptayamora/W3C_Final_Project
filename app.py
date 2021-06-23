from flask import Flask, render_template, request, redirect
from flask import g
import os
import sqlite3
import time

currentlocation = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

DATABASE = './Login.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connect(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def check_login(Username, Password):
    user = query_db('SELECT * FROM Users WHERE Username = ? and Password = ?', [Username, Password], one=True)
    if user is None:
        return False
    else:
        return True

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET'])
def login1():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login2():
    UN = request.form['Username']
    PW = request.form['Password']

    sqlconnection = sqlite3.Connection(currentlocation + '\Login.db')
    cursor = sqlconnection.cursor()
    query1 = "SELECT Username, Password FROM Users WHERE Username = '{un}' AND Password = '{pw}'".format(un = UN, pw = PW)

    check_rows = cursor.execute(query1)
    check_rows = check_rows.fetchall()

    error = None

    if len(check_rows) == 1:
        return redirect('/dashboard')
        #render will be changed dashboard still to be edited
    else:
        if check_login(request.form['Username'], request.form['Password']):
            return redirect('/register')
        else:
            error = 'Username and password not recognized'
            time.sleep(1)
            return render_template('login.html', error=error)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        rFN = request.form['RFirstname']
        rLN = request.form['RLastname']
        rUN = request.form['RUsername']
        rPW = request.form['RPassword']
        sqlconnection = sqlite3.Connection(currentlocation + '\Login.db')
        cursor = sqlconnection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        FirstName VARCHAR(20) NOT NULL,
        LastName VARCHAR(20) NOT NULL,
        Username VARCHAR(20) NOT NULL,
        Password VARCHAR(20) NOT NULL);
        ''')
        #makes table named Users if it doesnt exist

        query1 = "INSERT INTO Users VALUES('{f}','{l}','{u}','{p}')".format(f=rFN, l=rLN, u=rUN, p=rPW)
        cursor.execute(query1)
        sqlconnection.commit()
        return redirect('/')

    return render_template('register.html')
    #could not make function verifying if username is already taken

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    #very bare no design yet

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/vaccine')
def vaccine():
    return render_template('vaccine.html')

if __name__ == '__main__':
    app.run(debug=True)

#notes
#about contact faq and vaccine navbar could not make function where if user logged in correctly
#login and signup buttons will be replaced by logout or name
