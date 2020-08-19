import json
import hashlib
import random
from flask import Flask, render_template, request, redirect
import pymysql

from app import config

app = Flask(__name__)

blockchain_servers = [
    'https://e-voting-blockchain-core-1.herokuapp.com/',
    'https://e-voting-blockchain-core-2.herokuapp.com/',
    'https://e-voting-blockchain-core-3.herokuapp.com/'
]

connection = pymysql.connect(config.mysqlServer, config.mysqlUsername, config.mysqlPassword, config.mysqlDatabase)
cursor = connection.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/2')
def newIndex():
    return render_template('index2.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = dict(request.form)
        key = create_user(data)
        if key == '':
            return render_template('error.html', error='Unable to create Voter ID. Possibly a voter ID already exists with the same Aadhar ID.')
        return render_template('key.html', key=key)
        

@app.route('/register/success', methods=['POST', 'GET'])
def register_success():
    return render_template('register2.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/vote')
def vote():
    return render_template('vote.html')

@app.route('/vote/cast', methods=['GET', 'POST'])
def cast():
    return render_template('cast.html')

@app.route('/candidate_list')
def candidate_list():
    try:
        cursor.execute("select * from candidate_list;")
        rows = cursor.fetchall()
    except:
        check_mysql_connection(cursor)
        try:
            cursor.execute("select * from candidate_list;")
            rows = cursor.fetchall()
        except Exception as e:
            print(str(e))
            return render_template('error.html', error = "Error in fetching data from database.")
    candidateList = []
    for row in rows:
        candidateList.append({
            'candidate_id': row[0],
            'name': row[1],
            'party': row[2]
        })
    return render_template('cdl.html', candidateList = candidateList)
    


@app.route('/voter_list')
def voter_list():
    query = "select voter_id, name, voted from voter_list;"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except:
        check_mysql_connection(cursor)
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as e:
            print(str(e))
            return render_template('error.html', error="Error in fetching data from database.")
    voterList = []
    for row in rows:
        voterList.append({
            'voter_id': row[0],
            'name': row[1],
            'voted': row[2]
        })
    return render_template('admin.html', voterList=voterList)


@app.route('/create_user', methods=['POST'])        #TODO: use create_user function
def create_user_route():
    try:
        name = request.form['name']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        aadhar_id = request.form['aadhar_id']
        dob = request.form['dob']
        contact_no = request.form['contact_no']
        lst = [name, aadhar_id, dob, contact_no]
        key = hashlib.md5(str(lst).encode()).hexdigest()
        voter_id = int(aadhar_id[-5:]+ contact_no[-3:])
        print(voter_id)
        query = f'''insert into voter_list values({voter_id}, '{name}', '{password_hash}', {aadhar_id}, "{dob}", {contact_no}, "{key}", 0, 0);'''
        cursor.execute(query)
        connection.commit()
        return key
    except Exception as e:
        connection.rollback()
        print('Error: ', e)
    return '0'

@app.route('/get_candidates')
def get_candidates():
    pass

@app.route('/check_voter', methods=['POST'])
def check_candidate():
    try:
        name = request.form['name']
        aadhar_id = request.form['aadhar_id']
        password_hash = request.form['password_hash']
        key = request.form['key']
        cursor.execute('select * from voter_list where aadhar_id = %s', (aadhar_id))
        result = cursor.fetchone()
        if name == result[1] and password_hash == result[2] and key == result[6] and result[7] == 0 and result[8] == 1:
            return '1'
    except Exception as e:
        print('Error:', e)
    return '0'

def create_user(data : dict):
    check_mysql_connection(cursor)
    try:
        name = data['name']
        password = data['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        aadhar_id = data['aadhar_id']
        dob = data['dob']
        contact_no = data['contact_no']
        email = data['email']
        verified = 1               #verification automated
        lst = [name, aadhar_id, dob, contact_no, random.randrange(10**10)]
        key = hashlib.md5(str(lst).encode()).hexdigest()
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        cursor.execute("insert into voter_list (name, password_hash, aadhar_id, dob, email, contact_no, key_hash, voted, verified) values (%s, %s, %s, %s, %s, %s, %s, false, %s);", (
                name,
                password_hash,
                aadhar_id,
                dob,
                email,
                contact_no,
                key_hash,
                verified
        ))
        connection.commit()
        return key
    except Exception as e:
        connection.rollback()
        print('Error: ', e)
    return ''

def check_mysql_connection(cursor):
    try:
        cursor.execute("select * from sample_table where s_no=1;")
    except Exception as e1:
        print("Reconnecting to database server...")
        print(str(e1))
        try:
            connection = pymysql.connect(config.mysqlServer, config.mysqlUsername, config.mysqlPassword, config.mysqlDatabase)
            cursor = connection.cursor()
        except Exception as e:
            print("Error: Unable to connect to mySQL server.")
            print("Error: " + str(e))
    globals()['cursor'] = cursor
