import sqlite3
import os
from flask import g

db_path = './Form.db'

currentlocation = os.path.dirname(os.path.abspath(__file__))

DATABASE = './Login.db'

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

# Connect to DB and return Conn and Cur objects
def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    # convert tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# Read the user info
def read_data(data_id):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM data WHERE id=?'
    result = cur.execute(query, (data_id,)).fetchone()
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