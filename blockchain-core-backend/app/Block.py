import hashlib

class Block:
    
    def __init__(self, index, candidate_id, timestamp, proof, previous_hash):
        self.index = index
        self.candidate_id = candidate_id
        self.timestamp = timestamp
        self.proof = proof
        self.previous_hash = previous_hash
        self.hash = self.generate_hash()

    def generate_hash(self):
        lst = [self.index, self.candidate_id, self.timestamp, self.proof, self.previous_hash]
        s = str(lst).encode()
        return hashlib.sha256(s).hexdigest()