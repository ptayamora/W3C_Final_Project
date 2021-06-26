from flask import Flask, render_template, request, redirect
from data import *
import sqlite3
import time

app = Flask(__name__)

@app.teardown_appcontext
def close_connect(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET'])
def login1():
    return render_template('admin_login.html')

@app.route('/login', methods=['POST'])
def login2():
    UN = request.form['Username']
    PW = request.form['Password']

    sqlconnection = sqlite3.Connection(currentlocation + '\Login.db')
    cursor = sqlconnection.cursor()
    query = "SELECT Username, Password FROM Users WHERE Username = '{un}' AND Password = '{pw}'".format(un = UN, pw = PW)

    rows = cursor.execute(query)
    rows = rows.fetchall()

    error = None

    if len(rows) == 1:
        return redirect('/dashboard')
        #render will be changed dashboard still to be edited
    else:
        if check_login(request.form['Username'], request.form['Password']):
            return redirect('/dashboard')
        else:
            error = 'Username and password not recognized'
            time.sleep(1)
            return render_template('admin_login.html', error=error)

@app.route('/admin_register', methods = ['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        rFN = request.form['RFirstname']
        rLN = request.form['RLastname']
        rUN = request.form['RUsername']
        rPW = request.form['RPassword']
        sqlconnection = sqlite3.Connection(currentlocation + '/Login.db')
        cursor = sqlconnection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        ID INTEGER PRIMARY KEY AUTOINCREMENT
        FirstName VARCHAR(20) NOT NULL,
        LastName VARCHAR(20) NOT NULL,
        Username VARCHAR(20) NOT NULL,
        Password VARCHAR(20) NOT NULL);
        ''')
        #makes table named Users if it doesnt exist

        query1 = "INSERT INTO Users VALUES(null,'{f}','{l}','{u}','{p}')".format(f=rFN, l=rLN, u=rUN, p=rPW)
        cursor.execute(query1)
        sqlconnection.commit()
        return redirect('/')

    return render_template('admin_register.html')
    #could not make function verifying if username is already taken

@app.route('/dashboard')
def dashboard():
    sqlconnection = sqlite3.connect(currentlocation + '\Login.db')
    sqlconnection.row_factory = sqlite3.Row
    cur = sqlconnection.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    return render_template('dashboard.html', rows=rows)
    #very bare no design yet

@app.route('/register', methods=['get','post'])
def register():
    if request.method == 'POST':
        vCT = request.form['VCategory']
        vLN = request.form['VLastname']
        vFN = request.form['VFirstname']
        vMN = request.form['VMiddlename']
        vCN = request.form['VContactnumber']
        vEM = request.form['VEmail']
        vBM = request.form['VBirthmonth']
        vBD = request.form['VBirthdate']
        vBY = request.form['VBirthyear']
        vAG = request.form['VAge']
        vGN = request.form['VGender']
        vCS = request.form['VCivilstatus']
        vRG = request.form['VRegion']
        vPR = request.form['VProvince']
        vCY = request.form['VCity']
        vBR = request.form['VBarangay']
        vAD = request.form['VAddress']
        vPS = request.form['VPregnancystatus']
        vCI = request.form['VCovidinteraction']
        vAL = request.form['VAllergies']
        vAL2 = request.form['VAllergies2']
        vCM = request.form['VComorbidity']
        vSL = request.form['VSelection']
        vDG = request.form['VDiagnosis']
        vCL = request.form['VClassification']
        vCD = request.form['VCoviddate']
        vCO = request.form['VConsent']
        vUN = request.form['VUsername']
        vPW = request.form['VPassword']

        sqlconnection = sqlite3.Connection(currentlocation + '\Form.db')
        cursor = sqlconnection.cursor()

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS DATA(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category VARCHAR(20) NOT NULL,
                    last_name VARCHAR(20) NOT NULL,
                    first_name VARCHAR(20) NOT NULL,
                    mid_name VARCHAR(20) NOT NULL,
                    contact_num TEXT NOT NULL,
                    email TEXT NOT NULL,
                    birthmonth VARCHAR(20) NOT NULL,
                    birthdate INTEGER NOT NULL,
                    birthyear INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    gender VARCHAR(20) NOT NULL,
                    civil_status VARCHAR(20) NOT NULL,
                    region VARCHAR(20) NOT NULL,
                    province VARCHAR(20) NOT NULL,
                    city VARCHAR(20) NOT NULL,
                    barangay TEXT NOT NULL,
                    address TEXT NOT NULL,
                    pregnancy_status TEXT NOT NULL,
                    covid_interaction TEXT NOT NULL,
                    allergy TEXT NOT NULL,
                    allergy_list VARCHAR(100),
                    comorbidity TEXT NOT NULL,
                    selection VARCHAR(100),
                    diagnosis TEXT NOT NULL,
                    classification VARCHAR(100),
                    covid_date TEXT NOT NULL,
                    consent TEXT NOT NULL,
                    username VARCHAR(20) NOT NULL,
                    password VARCHAR(20) NOT NULL);
                    ''')

        query1 = "INSERT INTO DATA VALUES(null,'{ct}','{ln}','{fn}','{mn}','{cn}','{em}','{bm}','{bd}','{by}','{ag}','{gn}','{cs}','{rg}','{pr}','{cy}','{br}','{ad}','{ps}','{ci}','{al}','{al2}','{cm}','{sl}','{dg}','{cl}','{cd}','{co}','{un}','{pw}')".format(ct=vCT, ln=vLN, fn=vFN, mn=vMN, cn=vCN, em=vEM, bm=vBM, bd=vBD, by=vBY, ag=vAG, gn=vGN, cs=vCS, rg=vRG, pr=vPR, cy=vCY, br=vBR, ad=vAD, ps=vPS, ci=vCI, al=vAL, al2=vAL2, cm=vCM, sl=vSL, dg=vDG, cl=vCL, cd=vCD, co=vCO, un=vUN, pw=vPW)
        cursor.execute(query1)

        sqlconnection.commit()
        return redirect('/home')

    return render_template('register.html')

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
