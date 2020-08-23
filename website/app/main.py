import json
import hashlib
import random
import requests
import threading
from flask import Flask, render_template, request, redirect, session
import pymysql

from app import config

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #############WARNING: remove in production
app.secret_key = config.appSecretKey

blockchain_servers = [
    'https://e-voting-blockchain-core-1.herokuapp.com',
    'https://e-voting-blockchain-core-2.herokuapp.com',
    'https://e-voting-blockchain-core-3.herokuapp.com'
]

connection = pymysql.connect(config.mysqlServer, config.mysqlUsername, config.mysqlPassword, config.mysqlDatabase)
cursor = connection.cursor()

@app.route('/')
def index():
    return render_template('index.html', loggedin = isLoggedin())

@app.route('/2')
def newIndex():
    return render_template('index2.html')

@app.route('/key_test')
def key_test():
    return render_template('key.html', voter_id = 100000000031, key = 'akjdshiuh874r78h23r82938h3rh')

@app.route('/dashboard')
def dashboard():
    if isLoggedin():
        return render_template("dashboard.html", loggedin = True, username = session['name'])
    else:
        return redirect("/")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        if isLoggedin():
            return redirect('/')
        return render_template('register.html', loggedin = False)
    else:
        aadhar_id = request.form['aadhar_id']
        data = dict(request.form)
        key = create_user(data)
        if key == '':
            return render_template('error.html', error='Unable to create Voter ID. Possibly a voter ID already exists with the same Aadhar ID.')
        cursor.execute("select voter_id from voter_list where aadhar_id = %s", (aadhar_id))
        voter_id = cursor.fetchone()[0]
        return render_template('key.html', voter_id = voter_id, key=key)


@app.route('/results')
def results():                  ##################TODO
    candidateList2 = get_results()
    for candidate in candidateList2:
        print(candidate['votes'])
    candidateList = get_candidate_list()
    i = 100
    for candidate in candidateList:
        candidate['votes'] = i
        i += 50
    return render_template('results.html', candidateList = candidateList, loggedin = isLoggedin())


@app.route('/login', methods=['POST', 'GET'])
def vote():
    if request.method == 'POST':
        check_mysql_connection(cursor)
        try:
            name = request.form['name']
            voter_id = request.form['voter_id']
            password = request.form['password']
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("select name, password_hash from voter_list where voter_id = %s;", (voter_id))
            result = cursor.fetchone()
            if result is not None:
                if name == result[0] and password_hash == result[1]:
                    session.permanent = False
                    session['name'] = name
                    session['voter_id'] = voter_id
                    return redirect('/cast')
                else:
                    return render_template('login.html', warning="User name or password does not match. Try again.")
            else:
                return render_template('login.html', warning="Invalid Voter ID.")
        except Exception as e:
            print(str(e))
            return render_template('error.html', error="Unable to connect to the database. Please try again later.")
    else:
        if isLoggedin():
            return redirect('/')
        return render_template('login.html', loggedin = False)

@app.route('/cast', methods=['GET', 'POST'])
def cast():
    if isLoggedin():
        candidateList = get_candidate_list()
        return render_template('cast.html', candidateList=candidateList, loggedin = True, username = session['name'], voter_id = session['voter_id'], blockchain_servers = blockchain_servers)
    else:
        return redirect('/login')


@app.route('/candidate_list')
def candidate_list():
    candidateList = get_candidate_list()
    return render_template('cdl.html', candidateList = candidateList, loggedin = isLoggedin())


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
    return render_template('admin.html', voterList=voterList, loggedin = isLoggedin())

@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('voter_id', None)
    return redirect('/')


#################################################*Andriod App API Routes*#############################################

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
    candidateList = get_candidate_list()
    return candidateList

######################################################*Common*###########################################################



############################################*Blockchain server API routes*###############################################

@app.route('/api/voter_check', methods=['POST'])
def api_voter_check():
    voter_id = request.form['voter_id']
    key_hash = request.form['key_hash']
    error = ""
    query = "select key_hash, voted, verified from voter_list where voter_id = %s;"
    try:
        cursor.execute(query, (voter_id))
        result = cursor.fetchone()
    except:
        check_mysql_connection(cursor)
        try:
            cursor.execute(query, (voter_id))
            result = cursor.fetchone()
        except Exception as e:
            print(str(e))
            return {
                "status": 0,
                "error": "Unable to connect to the database."
            }

    if result is None:
        error = "Invalid Voter ID."
    else:
        voted = result[1]
        verified = result[2]
        if result[0] == key_hash:
            if verified == 1:
                if voted == 0:
                    return {"status": 1}
                else:
                    error = "Already Voted."
            else:
                error = "Voter ID not verified."
        else:
            error = "Incorrect Key."

    return {
        "status": 0,
        "error": error
    }

##############################################*Helper Functions*###########################################################

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


def get_candidate_list():
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
    return candidateList


def get_results():
    blockchainResponse = []
    def makeReq(server):
        blockchainResponse.append(requests.get(server + '/get_result').text)
    reqs = []
    for server in blockchain_servers:
        reqs.append(threading.Thread(target=makeReq, args=[server]))
        reqs[-1].start()
    for req in reqs:
        req.join()
    similarResponse = {}
    for res in blockchainResponse:
        if res in similarResponse:
            similarResponse[res] += 1
        else:
            similarResponse[res] = 1
    resultStr = ''
    maxCount = 0
    for res in similarResponse:
        if similarResponse[res] > maxCount:
            maxCount = similarResponse[res]
            resultStr = res
    result = json.loads(resultStr)
    
    candidateList = get_candidate_list()
    for candidate in candidateList:
        if str(candidate['candidate_id']) in result:
            candidate['votes'] = result[str(candidate['candidate_id'])]
        else:
            candidate['votes'] = 0
    return candidateList

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

def isLoggedin() -> bool:
    if 'name' in session and 'voter_id' in session:
        return True
    return False