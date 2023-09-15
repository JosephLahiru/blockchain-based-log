import hashlib
import datetime
import pickle


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash


class Blockchain:
    def __init__(self, filename='blockchain.p'):
        self.filename = filename
        try:
            self.chain = self.load_blockchain()
            self.previous_block = self.chain[-1]
        except (FileNotFoundError, EOFError):
            self.chain = [self.create_genesis_block()]
            self.previous_block = self.chain[0]

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def create_genesis_block(self):
        return Block(0, '0', datetime.datetime.now(), 'Genesis Block', self.calculate_hash(0, '0', datetime.datetime.now(), 'Genesis Block'))

    def create_new_block(self, data):
        index = self.previous_block.index + 1
        timestamp = datetime.datetime.now()
        hash = self.calculate_hash(
            index, self.previous_block.hash, timestamp, data)
        return Block(index, self.previous_block.hash, timestamp, data, hash)

    def add_block(self, data):
        new_block = self.create_new_block(data)
        self.chain.append(new_block)
        self.previous_block = new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != self.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def save_blockchain(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.chain, f)

    def load_blockchain(self):
        with open(self.filename, 'rb') as f:
            return pickle.load(f)

    def exit_handler(self):
        self.save_blockchain()
