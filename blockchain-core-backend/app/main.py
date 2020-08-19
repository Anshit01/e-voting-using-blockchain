from flask import Flask, request
from flask_cors import CORS
import requests
import json
from app.Blockchain import Blockchain
import hashlib

server = 'https://e-voting-blockchain-website.herokuapp.com'

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()

@app.route('/')
def index():
    return 'Index'

@app.route('/get_blockchain')
def get_blockchain():
    return blockchain.get_blockchain()

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    voter_id = request.form['voter_id']
    key = request.form['key']
    candidate_id = request.form['candidate_id']
    payload = {'voter_id': voter_id, 'key': key}
    r = requests.post(server+'/check_voter', data=payload)
    if r.text == '1':
        blockchain.add_block(candidate_id)
        return '1'
    return '0'

@app.route('/get_result')
def get_result():
    chain = blockchain.chain
    result = {}
    for block in chain:
        candidate_id = block.candidate_id
        if candidate_id in result:
            result[candidate_id] += 1
        else:
            result[candidate_id] = 1
    return result
        
        

if(__name__ == '__main__'):
    app.run(debug=True)