from flask import Flask, request
from flask_cors import CORS
import requests
import json
from app.Blockchain import Blockchain
import hashlib

server = 'https://e-voting-blockchain-website.herokuapp.com/api'

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
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    candidate_id = request.form['candidate_id']
    payload = {'voter_id': voter_id, 'key_hash': key_hash}
    r = requests.post(server+'/voter_check', data=payload)
    response = r.json()
    if response['status'] == 1:
        blockchain.add_block(candidate_id)
    return response

@app.route('/get_result')
def get_result():
    chain = json.loads(blockchain.get_blockchain())
    chain = chain[1:]
    result = {}
    for block in chain:
        candidate_id = block['candidate_id']
        if candidate_id in result:
            result[candidate_id] += 1
        else:
            result[candidate_id] = 1
    return result
        
