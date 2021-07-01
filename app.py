from flask import Flask, render_template, redirect, request
from data import *
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

def login1():
    return redirect('/admin_dashboard')

@app.route('/admin_login', methods=['GET','POST'])
def login2():
    error = None
    if request.method == 'POST':
        if check_login(request.form['Username'], request.form['Password']):
            return login1()
        else:
            error = 'Username and password not recognized'
    return render_template('admin_login.html', error=error)

@app.route('/admin_dashboard')
def dashboard1():
    data = read_all()
    return render_template('admin_dashboard.html', data=data)

@app.route('/admin_register', methods=['GET'])
def admin_register1():
    return render_template('admin_register.html')

@app.route('/admin_register', methods = ['POST'])
def admin_register2():
    admin_data = {'firstName':request.form['RFirstname'],
                  'lastName':request.form['RLastname'],
                  'userName':request.form['RUsername'],
                  'passWord':request.form['RPassword']
                 }

    create_table_admin()
    register_admin(admin_data)
    time.sleep(1)
    return redirect('/admin_login')

@app.route('/modify/<int:data_id>', methods=['POST'])
def modify(data_id):
    data = read_data_by_id(data_id)
    if request.form['action'] == 'View':
        return render_template('admin_view.html',data=data)
    elif request.form['action'] == 'Edit':
        return render_template('edit_form.html', data=data)
    elif request.form['action'] == 'Delete':
        delete_record(data_id)
        time.sleep(0.5)
        return dashboard1()
    else:
        return dashboard1()

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

        create_table_customer()
        insert_info(vac_data)
        time.sleep(1)
        return redirect('/home')

def login3(Username):
    DATA = read_data(Username)
    return render_template('customer_view.html',data=DATA)

@app.route('/customer', methods=['GET','POST'])
def login4():
    error = None
    if request.method == 'POST':
        if check_login2(request.form['Username'], request.form['Password']):
            return login3(request.form['Username'])
        else:
            error = 'Username and password not recognized'
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

