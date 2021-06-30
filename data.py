import sqlite3
import os
from flask import g

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

def create_table_customer():
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
                region VARCHAR(50) NOT NULL,
                province VARCHAR(50) NOT NULL,
                city VARCHAR(50) NOT NULL,
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
                vaccine_status VARCHAR(50),
                vaccine VARCHAR(50),
                username VARCHAR(20) NOT NULL,
                password VARCHAR(20) NOT NULL);
                '''
    cur.execute(query)
    conn.commit()
    conn.close()

def create_table_admin():
    conn, cur = connect_db(DATABASE)
    query = '''
            CREATE TABLE IF NOT EXISTS Users(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName VARCHAR(20) NOT NULL,
            LastName VARCHAR(20) NOT NULL,
            Username VARCHAR(20) NOT NULL,
            Password VARCHAR(20) NOT NULL);
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

def read_data_by_id(data_id):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM DATA WHERE id=?'
    result = cur.execute(query, (data_id,)).fetchone()
    conn.close()
    return result

# Insert info to DB
def insert_info(vac_data):
    conn, cur = connect_db(db_path)
    query = 'INSERT INTO data (category, last_name, first_name, mid_name, contact_num, email, birthmonth, birthdate, birthyear, age, gender, civil_status, region, province, city, barangay, address, pregnancy_status, covid_interaction, allergy, allergy_list, comorbidity, selection, diagnosis, classification, covid_date, consent, username, password) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    values = (vac_data['category'],
              vac_data['l_name'],
              vac_data['f_name'],
              vac_data['m_name'],
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
              vac_data['preg_stat'],
              vac_data['covid_interaction'],
              vac_data['allergy'],
              vac_data['allergy_list'],
              vac_data['comorbidity'],
              vac_data['selection'],
              vac_data['diagnosis'],
              vac_data['classification'],
              vac_data['covid_date'],
              vac_data['consent'],
              vac_data['username'],
              vac_data['password'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

def register_admin(admin_data):
    conn, cur = connect_db(DATABASE)
    query = 'INSERT INTO Users (FirstName, LastName, Username, Password) VALUES(?,?,?,?)'
    values = (admin_data['firstName'],
              admin_data['lastName'],
              admin_data['userName'],
              admin_data['passWord']
              )
    cur.execute(query, values)
    conn.commit()
    conn.close()

def update_data(vac_data):
    conn, cur = connect_db(db_path)
    query = 'UPDATE DATA SET vaccine_status=?,vaccine=? WHERE id=?'
    values = (vac_data['vaccine_status'],
              vac_data['vaccine'],
              vac_data['id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

def delete_record(data_id):
    conn, cur = connect_db(db_path)
    query = 'DELETE FROM DATA WHERE id=?'
    cur.execute(query, (data_id,))
    conn.commit()
    conn.close()