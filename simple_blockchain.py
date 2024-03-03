import hashlib
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, difficulty):
        self.nonce = 0
        computed_hash = self.compute_hash()
        while not computed_hash.startswith('0' * difficulty):
            self.nonce += 1
            computed_hash = self.compute_hash()
        self.hash = computed_hash
        return computed_hash

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.difficulty = 2
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.chain[-1]

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        new_block.proof_of_work(self.difficulty)
        self.chain.append(new_block)
        self.unconfirmed_transactions = []
        return new_block.index

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.compute_hash():
                print("Current hash does not match")
                return False
            
            if current.previous_hash != previous.hash:
                print("Previous hash does not match")
                return False
            
            if not current.hash.startswith('0' * self.difficulty):
                print("Proof of work is invalid")
                return False
        return True

# Example 
blockchain = Blockchain()
blockchain.add_new_transaction("Alice pays Bob 1 BTC")
blockchain.add_new_transaction("Bob pays Charlie 0.5 BTC")
blockchain.mine()

blockchain.add_new_transaction("Charlie pays Dave 0.2 BTC")
blockchain.mine()

print("Blockchain is valid:", blockchain.is_chain_valid())

for block in blockchain.chain:
    print(f"Index: {block.index}, Transactions: {block.transactions}, Hash: {block.hash}")
