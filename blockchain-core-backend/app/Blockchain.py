from app.Block import Block
import datetime
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        block = Block(0, '0', self.get_timestamp(), '0', '0')
        self.chain.append(block)

    def add_block(self, candidate_id):
        proof = self.proof_of_work(self.chain[-1].proof)
        block = Block(len(self.chain), candidate_id, self.get_timestamp(), proof, self.chain[-1].hash)
        self.chain.append(block)

    def get_blockchain(self):
        lst = [self.parse_block_to_dict(block) for block in self.chain]
        s = json.dumps(lst)
        return s

    def parse_block_to_dict(self, block):
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
            if hash_code[:3] == '000':
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