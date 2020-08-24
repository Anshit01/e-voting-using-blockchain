from app.Block import Block
from app import config
from pymongo import MongoClient
import datetime
import hashlib
import json

cluster = MongoClient(f"mongodb+srv://{(config.username)}:{(config.password)}@cluster0.j2n3h.mongodb.net/{(config.username)}?retryWrites=true&w=majority")
collection = cluster[config.username].blockchain


class Blockchain:
    def __init__(self):
        blockCount = collection.count_documents({})
        if blockCount == 0:
            block = Block(0, '0', self.get_timestamp(), '0', '0')
            collection.insert_one(block.toDict())
        else:
            blockData = collection.find().skip(collection.count_documents({}) - 1)[0]
            block = self.blockFromData(blockData)
        self.lastBlock = block

    def blockFromData(self, data : dict) -> Block:
        return Block(
            data['index'],
            data['candidate_id'],
            data['timestamp'],
            data['proof'],
            data['previous_hash']
        )

    def add_block(self, candidate_id):
        proof = self.proof_of_work(self.lastBlock.proof)
        count = collection.count_documents({})
        block = Block(count, candidate_id, self.get_timestamp(), proof, self.lastBlock.hash)
        collection.insert_one(block.toDict())
        self.lastBlock = block

    def get_blockchain(self):
        data = list(collection.find({}))
        for doc in data:
            doc.pop('_id')
        return json.dumps(data)

    def parse_block_to_dict(self, block : Block):
        dictionary = {'index': block.index,
                      'candidate_id' : block.candidate_id,
                      'timestamp' : block.timestamp,
                      'proof' : block.proof,
                      'previous_hash' : block.previous_hash,
                      'hash' : block.hash}
        return dictionary

    def proof_of_work(self, previous_proof):
        new_proof = '0'
        int_proof = 0
        
        is_correct = False
        while not is_correct:
            hash_code = hashlib.sha256((previous_proof*2 + new_proof*2).encode()).hexdigest()
            #### Increase the 0's in the following string to increase the difficulty of generating proof of work.
            #### Adding one 0 increases the time by about 10x.
            #### A string with 3 zeros ('000') takes about 0.5 seconds on a normal PC.
            if hash_code[:3] == '00':
                is_correct = True
            int_proof += 1
            new_proof = self.int_to_str(int_proof)
        return new_proof

    def int_to_str(self, num):
        lst = [chr(ord('0') + i) for i in range(10)] + [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i) for i in range(26)]
        s = ''
        while num > 0:
            i = num % 62
            num //= 62
            s += lst[i]
        return s


    def get_timestamp(self):
        return str(datetime.datetime.now())