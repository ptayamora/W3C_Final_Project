import sqlite3
import os
from flask import g, request

currentlocation = os.path.dirname(os.path.abspath(__file__))

DATABASE = './Login.db'

db_path = './Form.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

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

def get_db2():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db

def query_db2(query, args=(), one=False):
    cur = get_db2().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def check_login2(Username, Password):
    user = query_db2('SELECT * FROM DATA WHERE username = ? and password = ?', [Username, Password], one=True)
    if user is None:
        return False
    else:
        return True

# Connect to DB and return Conn and Cur objects
def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    # convert tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

def create_table():
    conn, cur = connect_db(db_path)
    query = '''CREATE TABLE IF NOT EXISTS DATA(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category VARCHAR(20) NOT NULL,
                last_name VARCHAR(20) NOT NULL,
                first_name VARCHAR(20) NOT NULL,
                mid_name VARCHAR(20),
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
                '''
    cur.execute(query)

    conn.commit()
    conn.close()

# Read the user info
def read_data(username):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM DATA WHERE username=?'
    result = cur.execute(query, (username,)).fetchone()
    conn.close()
    return result

# Insert info to DB
def insert_info(vac_data):
    conn, cur = connect_db(db_path)
    query = 'INSERT INTO data (category, last_name, first_name, mid_name, suffix, contact_num, email, birthmonth, birthdate, birthyear, age, gender, civil_status, region, province, city, barangay, complete_address, covid_interaction, pregnant_status, allegies, comorbidity, selection, diagnosis, covid_classification, covid_date, consent) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    values = (vac_data['category'],
              vac_data['l_name'],
              vac_data['f_name'],
              vac_data['m_name'],
              vac_data['s_name'],
              vac_data['con_num'],
              vac_data['email_add'],
              vac_data['birth_month'],
              vac_data['birth_date'],
              vac_data['birth_year'],
              vac_data['age'],
              vac_data['gender'],
              vac_data['civil_stat'],
              vac_data['add_reg'],
              vac_data['add_prov'],
              vac_data['add_city'],
              vac_data['add_bar'],
              vac_data['address'],
              vac_data['Covid Interaction'],
              vac_data['preg_stat'],
              vac_data['Allergies'],
              vac_data['Comorbidity'],
              vac_data['selection'],
              vac_data['Diagnosis'],
              vac_data['classification'],
              vac_data['covid_date'],
              vac_data['Consent'])
    cur.execute(query, values)

    conn.commit()
    conn.close()

def update_record(username):
    if request.method == 'POST':
        eCT = request.form['ECategory']
        eLN = request.form['ELastname']
        eFN = request.form['EFirstname']
        eMN = request.form['EMiddlename']
        eCN = request.form['EContactnumber']
        eEM = request.form['EEmail']
        eBM = request.form['EBirthmonth']
        eBD = request.form['EBirthdate']
        eBY = request.form['EBirthyear']
        eAG = request.form['EAge']
        eGN = request.form['EGender']
        eCS = request.form['ECivilstatus']
        eRG = request.form['ERegion']
        ePR = request.form['EProvince']
        eCY = request.form['ECity']
        eBR = request.form['EBarangay']
        eAD = request.form['EAddress']
        ePS = request.form['EPregnancystatus']
        eCI = request.form['ECovidinteraction']
        eAL = request.form['EAllergies']
        eAL2 = request.form['EAllergies2']
        eCM = request.form['EComorbidity']
        eSL = request.form['ESelection']
        eDG = request.form['EDiagnosis']
        eCL = request.form['EClassification']
        eCD = request.form['ECoviddate']
        eCO = request.form['EConsent']
        eUN = request.form['EUsername']
        ePW = request.form['EPassword']

    conn, cur = connect_db(db_path)
    query = "UPDATE DATA SET VALUES(null,'{ct}','{ln}','{fn}','{mn}','{cn}','{em}','{bm}','{bd}','{by}','{ag}','{gn}','{cs}','{rg}','{pr}','{cy}','{br}','{ad}','{ps}','{ci}','{al}','{al2}','{cm}','{sl}','{dg}','{cl}','{cd}','{co}',null,null)".format(
        ct=eCT, ln=eLN, fn=eFN, mn=eMN, cn=eCN, em=eEM, bm=eBM, bd=eBD, by=eBY, ag=eAG, gn=eGN, cs=eCS, rg=eRG, pr=ePR,
        cy=eCY, br=eBR, ad=eAD, ps=ePS, ci=eCI, al=eAL, al2=eAL2, cm=eCM, sl=eSL, dg=eDG, cl=eCL, cd=eCD, co=eCO)
    cur.execute(query, (username),)
    conn.commit()
    conn.close()