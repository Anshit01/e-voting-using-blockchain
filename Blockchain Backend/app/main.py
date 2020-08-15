from flask import Flask, request
import requests
import json
from app.Blockchain import Blockchain
import hashlib

server = 'http://127.0.0.1:5001'

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/')
def index():
    return 'Index'

@app.route('/get_blockchain')
def get_blockchain():
    return blockchain.get_blockchain()

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    name = request.form['name']
    aadhar_id = request.form['aadhar_id']
    password = request.form['password']
    password_hash = hashlib.sha256(str(password).encode()).hexdigest()
    key = request.form['key']
    candidate_id = request.form['candidate_id']
    payload = {'name': name, 'aadhar_id': aadhar_id, 'password_hash': password_hash, 'key': key}
    r = requests.post(server+'/check_voter', data=payload)
    if r.text == '1':
        blockchain.add_block(candidate_id)
        return '1'
    return '0'

@app.route('/get_result')
def get_result():
    chain = blockchain.chain
    result = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0}
    for block in chain:
        candidate_id = block.candidate_id[-1]
        if candidate_id == '1':
            result['A'] += 1
        elif candidate_id == '2':
            result['B'] += 1
        elif candidate_id == '3':
            result['C'] += 1
        elif candidate_id == '4':
            result['D'] += 1
        elif candidate_id == '5':
            result['E'] += 1
    return json.dumps(result)
        
        

if(__name__ == '__main__'):
    app.run(debug=True)