from flask import Flask, render_template, redirect, url_for, request
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

@app.route('/admin_login', methods = ['GET'])
def login1():
    return render_template('admin_login.html')

@app.route('/admin_login', methods=['POST'])
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
        return redirect('/admin_dashboard')
    else:
        if check_login(request.form['Username'], request.form['Password']):
            return redirect('/admin_dashboard')
        else:
            error = 'Username and password not recognized'
            time.sleep(1)
            return render_template('admin_login.html', error=error)

@app.route('/admin_dashboard')
def dashboard():
    sqlconnection = sqlite3.connect(currentlocation + '\Form.db')
    sqlconnection.row_factory = sqlite3.Row
    cur = sqlconnection.cursor()
    cur.execute("SELECT * FROM DATA")
    data = cur.fetchall()
    return render_template('admin_dashboard.html', data=data)
    #very bare no design yet

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

@app.route('/modify/<int:data_id>', methods=['POST'])
def modify(data_id):
    data = read_data_by_id(data_id)
    if request.form['action'] == 'View':
        return render_template('admin_view.html',data=data)
    elif request.form['action'] == 'Edit':
        return render_template('edit_form.html', data=data)
    elif request.form['action'] == 'Delete':
        delete_record(data_id)
        time.sleep(1)
        return redirect(url_for('dashboard'))
    else:
        return redirect('/admin_dashboard')

@app.route('/view_record/<int:data_id>',methods=['POST'])
def view_record(data_id):
    if request.form['action'] == 'Back':
        return redirect('/admin_dashboard')
    else:
        return redirect('/home')

@app.route('/edit_record/<int:data_id>', methods=['POST'])
def update2(data_id):
    customer_vaccine_status =request.form['customer_vaccine_status']
    customer_vaccine = request.form['customer_vaccine']

    vac_data = {
        'vaccine_status':customer_vaccine_status,
        'vaccine':customer_vaccine,
        'id':data_id
    }

    update_data(vac_data)

    return redirect('/admin_dashboard')
    pass

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/processing', methods=['POST'])
def process():
        vac_data = {'category':request.form['VCategory'],
                    'l_name':request.form['VLastname'],
                    'f_name':request.form['VFirstname'],
                    'm_name': request.form['VMiddlename'],
                    'con_num': request.form['VContactnumber'],
                    'email_add': request.form['VEmail'],
                    'birth_month': request.form['VBirthmonth'],
                    'birth_date': request.form['VBirthdate'],
                    'birth_year': request.form['VBirthyear'],
                    'age': request.form['VAge'],
                    'gender': request.form['VGender'],
                    'civil_stat': request.form['VCivilstatus'],
                    'add_reg': request.form['VRegion'],
                    'add_prov': request.form['VProvince'],
                    'add_city': request.form['VCity'],
                    'add_bar': request.form['VBarangay'],
                    'address': request.form['VAddress'],
                    'preg_stat': request.form['VPregnancystatus'],
                    'covid_interaction': request.form['VCovidinteraction'],
                    'allergy': request.form['VAllergies'],
                    'allergy_list': request.form['VAllergies2'],
                    'comorbidity': request.form['VComorbidity'],
                    'selection': request.form['VSelection'],
                    'diagnosis': request.form['VDiagnosis'],
                    'classification': request.form['VClassification'],
                    'covid_date': request.form['VCoviddate'],
                    'consent': request.form['VConsent'],
                    'username': request.form['VUsername'],
                    'password': request.form['VPassword']}

        create_table()
        insert_info(vac_data)
        time.sleep(1)
        return redirect('/home')

@app.route('/customer', methods = ['GET'])
def login3():
    return render_template('customer_login.html')

@app.route('/customer', methods=['POST'])
def login4():
    UN = request.form['Username']
    PW = request.form['Password']

    sqlconnection = sqlite3.Connection(currentlocation + '\Form.db')
    cursor = sqlconnection.cursor()
    query = "SELECT Username, Password FROM DATA WHERE username = '{un}' AND password = '{pw}'".format(un = UN, pw = PW)

    rows = cursor.execute(query)
    rows = rows.fetchall()

    error = None

    if len(rows) == 1:
        DATA = read_data(UN)
        return render_template('customer_view.html', data=DATA)
    else:
        if check_login2(request.form['Username'], request.form['Password']):
            DATA = read_data(UN)
            return render_template('customer_view.html', data=DATA)
        else:
            error = 'Username and password not recognized'
            time.sleep(1)
            return render_template('customer_login.html', error=error)

@app.route('/customer', methods=['POST'])
def customer_back():
    if request.form['action'] == 'Logout':
        return redirect('/customer_login')
    else:
        return redirect('/home')

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

