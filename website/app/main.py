import json
import hashlib
from flask import Flask, render_template, request
import pymysql

app = Flask(__name__, static_folder='app/static/')

blockchain_servers = ['https://272e9d8b.ngrok.io', 'https://47ce0640.ngrok.io/', '']

# connection = pymysql.connect('localhost', 'root', '1234', 'e_voting')
# cursor = connection.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/2')
def newIndex():
    return render_template('index2.html')

@app.route('/register')
def register():
    return render_template('register.html')

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
    return render_template('cdl.html')

@app.route('/voter_list')
def voter_list():
    return render_template('admin.html')


@app.route('/create_user', methods=['POST'])
def create_user():
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
        cursor.execute(f'''select * from voter_list where aadhar_id = {aadhar_id}''')
        result = cursor.fetchone()
        if name == result[1] and password_hash == result[2] and key == result[6] and result[7] == 0 and result[8] == 1:
            return '1'
    except Exception as e:
        print('Error:', e)
    return '0'


if __name__ == '__main__':
    app.run(debug=True)