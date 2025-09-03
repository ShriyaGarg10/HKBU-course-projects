# -*- coding: utf-8 -*-
"""group3_mini blockchain

References

1.	https://pypi.org/project/cryptography/
2.	https://pypi.org/project/securesystemslib/0.14.2/
3.	https://docs.python.org/3/library/datetime.html
4.	https://docs.python.org/3/library/typing.html
5.	https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
6.	https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/
7.	https://commons.apache.org/proper/commons-codec/apidocs/org/apache/commons/codec/digest/DigestUtils.html
8.	https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
9.	https://en.bitcoin.it/wiki/Protocol_documentation#Merkle_Trees
10.	https://docs.python.org/3/library/hashlib.html
11.	https://www.analyticsvidhya.com/blog/2022/06/building-a-blockchain-in-python/
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import hashlib
from datetime import datetime
from typing import List
import time

# 4.1 Transaction Generation

class Account:
    def __init__(self, name):
        self.name = name
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def get_private_key_pem(self):
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

    def get_public_key_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    def get_address(self):
        return hashlib.sha256(self.get_public_key_pem().encode()).hexdigest()

    def sign_data(self, data):
        signature = self.private_key.sign(
            data.encode(),
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA256()
        )
        return signature.hex()

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now().isoformat()
        self.signature = None
        self.tid = None

    def sign(self, sender_account):
        transaction_data = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        self.signature = sender_account.sign_data(transaction_data)
        self.tid = self.calculate_tid()

    def calculate_tid(self):
        if not self.signature:
            raise ValueError("Transaction must be signed before calculating TID")
        transaction_content = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}{self.signature}"
        return hashlib.sha256(transaction_content.encode()).hexdigest()

    def to_dict(self):
        return {
            'tid': self.tid,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

def create_sample_transactions(num_transactions):
    alice = Account("Alice")
    bob = Account("Bob")
    charlie = Account("Charlie")
    dave = Account("Dave")

    transaction_data = [
        (alice, bob, 100),
        (bob, charlie, 50),
        (charlie, dave, 75),
        (dave, alice, 25),
        (alice, charlie, 60),
        (bob, dave, 85),
        (charlie, alice, 40),
        (dave, bob, 95)
    ]

    transactions = []
    for sender, receiver, amount in transaction_data[:num_transactions]:
        tx = Transaction(
            sender=sender.get_address(),
            receiver=receiver.get_address(),
            amount=amount
        )
        tx.sign(sender)
        transactions.append(tx)

    return transactions

# 4.2 Verifiable Merkle Tree

class MerkleNode:
    def __init__(self, hash_value: str, left=None, right=None):
        self.hash = hash_value
        self.left = left
        self.right = right

class MerkleTree:
    def __init__(self, transactions: List[Transaction]):
        if not transactions:
            raise ValueError("Cannot create a Merkle Tree with no transactions")
        if not self._is_power_of_two(len(transactions)):
            raise ValueError("Number of transactions must be a power of 2")
        self.transactions = transactions
        self.leaves = []
        self.root = None
        self._build_tree()

    def _is_power_of_two(self, n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0

    def _hash_pair(self, left: str, right: str) -> str:
        left_bytes = bytes.fromhex(left)
        right_bytes = bytes.fromhex(right)
        combined = left_bytes + right_bytes
        return hashlib.sha256(combined).hexdigest()

    def _build_tree(self):
        self.leaves = [
            MerkleNode(tx.calculate_tid())
            for tx in self.transactions
        ]

        print("\n=== Building Merkle Tree ===")
        print("Leaf nodes:")
        for i, leaf in enumerate(self.leaves):
            print(f"Leaf {i}: {leaf.hash}")

        current_level = self.leaves
        level = 0
        while len(current_level) > 1:
            next_level = []
            print(f"\nLevel {level}:")
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1]
                parent_hash = self._hash_pair(left.hash, right.hash)
                print(f"Combining {left.hash[:8]}... and {right.hash[:8]}... -> {parent_hash[:8]}...")
                parent = MerkleNode(parent_hash, left, right)
                next_level.append(parent)
            current_level = next_level
            level += 1

        self.root = current_level[0]
        print(f"\nRoot hash: {self.root.hash}")

    def get_root_hash(self) -> str:
        return self.root.hash if self.root else None

    def verify_transaction(self, transaction: Transaction, proof: List[str]) -> bool:
        print("\n=== Verifying Transaction ===")
        current_hash = transaction.calculate_tid()
        print(f"Starting with transaction hash: {current_hash}")

        try:
            current_index = next(i for i, tx in enumerate(self.transactions) if tx.tid == transaction.tid)
        except StopIteration:
            return False

        print(f"Transaction found at index: {current_index}")

        for level, sibling_hash in enumerate(proof):
            is_left = (current_index % 2) == 0
            old_hash = current_hash

            if is_left:
                print(f"Level {level}: Combining left={old_hash[:8]}... with right={sibling_hash[:8]}...")
                current_hash = self._hash_pair(old_hash, sibling_hash)
            else:
                print(f"Level {level}: Combining left={sibling_hash[:8]}... with right={old_hash[:8]}...")
                current_hash = self._hash_pair(sibling_hash, old_hash)

            print(f"-> Result: {current_hash[:8]}...")
            current_index //= 2

        print(f"\nFinal computed hash: {current_hash}")
        print(f"Expected root hash:   {self.get_root_hash()}")
        return current_hash == self.get_root_hash()

    def get_proof(self, transaction_index: int) -> List[str]:
        if transaction_index < 0 or transaction_index >= len(self.transactions):
            raise ValueError("Transaction index out of range")

        print("\n=== Generating Merkle Proof ===")
        print(f"Generating proof for transaction at index {transaction_index}")

        proof = []
        current_level = self.leaves.copy()
        current_index = transaction_index

        while len(current_level) > 1:
            print(f"\nLevel with {len(current_level)} nodes:")
            sibling_index = current_index + 1 if current_index % 2 == 0 else current_index - 1
            sibling_hash = current_level[sibling_index].hash
            proof.append(sibling_hash)

            target_hash = current_level[current_index].hash
            is_left = current_index % 2 == 0
            if is_left:
                print(f"Target (left) {target_hash[:8]}... with sibling (right) {sibling_hash[:8]}...")
            else:
                print(f"Sibling (left) {sibling_hash[:8]}... with target (right) {target_hash[:8]}...")

            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1]
                parent_hash = self._hash_pair(left.hash, right.hash)
                next_level.append(MerkleNode(parent_hash))
                if i == (current_index // 2) * 2:
                    print(f"Combined to parent: {parent_hash[:8]}...")

            current_level = next_level
            current_index //= 2

        return proof

# 4.3 Construction of Blockchain

class Block:
    def __init__(self, transactions, previous_hash="0"):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.merkle_root = self.calculate_merkle_root()
        self.current_hash = self.mine_block()

    def calculate_merkle_root(self):
        merkle_tree = MerkleTree(self.transactions)
        return merkle_tree.get_root_hash()

    def calculate_hash(self):
        block_header = f"{self.previous_hash}{self.merkle_root}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_header.encode()).hexdigest()

    def mine_block(self, difficulty=4):
        print(f"Mining block with difficulty {difficulty}...")
        target_prefix = "0" * difficulty
        while not self.calculate_hash().startswith(target_prefix):
            self.nonce += 1
        print(f"Block mined! Nonce: {self.nonce}, Hash: {self.calculate_hash()}")
        return self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        print("\n=== Creating Genesis Block ===")
        genesis_transaction = Transaction("GENESIS", "NETWORK", 0)
        genesis_transaction.sign(Account("GENESIS"))
        return Block([genesis_transaction])

    def add_block(self, transactions):
        previous_hash = self.chain[-1].current_hash
        new_block = Block(transactions, previous_hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        print("\n=== Verifying Blockchain Integrity ===")
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.current_hash:
                print(f"Error: Block {i} has an invalid previous hash!")
                return False

            if current_block.calculate_hash() != current_block.current_hash:
                print(f"Error: Block {i} has been tampered with!")
                return False

        print("Blockchain is valid!")
        return True

# 4.4 Mining a Block

class Miner:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.target = "0" * difficulty

    def mine_block(self, block):
        """
        Implements the Proof-of-Work protocol for mining a block.
        1. Combines all block information
        2. Starts with nonce = 0
        3. Calculates SHA-256 hash
        4. Checks if hash meets target difficulty
        """
        print(f"\n=== Mining Block with Difficulty {self.difficulty} ===")
        start_time = time.time()

        while True:
            current_hash = block.calculate_hash()
            if current_hash.startswith(self.target):
                end_time = time.time()
                print(f"Block mined! Time taken: {end_time - start_time:.2f} seconds")
                print(f"Nonce found: {block.nonce}")
                print(f"Block hash: {current_hash}")
                return current_hash
            block.nonce += 1
            if block.nonce % 100000 == 0:
                print(f"Tried {block.nonce} nonces...")

# 4.5 Integrity Verification Implementation

class BlockchainVerifier:
    @staticmethod
    def verify_transaction_signature(transaction, public_key_pem):
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode()
            )
            transaction_data = f"{transaction.sender}{transaction.receiver}{transaction.amount}{transaction.timestamp}"
            signature_bytes = bytes.fromhex(transaction.signature)

            public_key.verify(
                signature_bytes,
                transaction_data.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {str(e)}")
            return False

    @staticmethod
    def verify_block_integrity(block):
        print("\n=== Verifying Block Integrity ===")

        calculated_hash = block.calculate_hash()
        if calculated_hash != block.current_hash:
            print("Block hash verification failed!")
            return False

        merkle_tree = MerkleTree(block.transactions)
        if merkle_tree.get_root_hash() != block.merkle_root:
            print("Merkle root verification failed!")
            return False

        print("Block integrity verified successfully!")
        return True

    @staticmethod
    def simulate_attack(blockchain):
        print("\n=== Simulating Blockchain Attacks ===")

        if len(blockchain.chain) < 2:
            print("Need at least 2 blocks to simulate attacks")
            return

        # 1. Attempt to modify transaction amount
        print("\n1. Attempting to modify transaction amount...")
        target_block = blockchain.chain[1]
        if target_block.transactions:
            original_amount = target_block.transactions[0].amount
            target_block.transactions[0].amount += 100
            print(f"Modified transaction amount from {original_amount} to {original_amount + 100}")
            print("Integrity check after modification:", BlockchainVerifier.verify_block_integrity(target_block))
            target_block.transactions[0].amount = original_amount

        # 2. Attempt to modify block timestamp
        print("\n2. Attempting to modify block timestamp...")
        original_timestamp = target_block.timestamp
        target_block.timestamp = time.time()
        print("Modified block timestamp")
        print("Integrity check after modification:", BlockchainVerifier.verify_block_integrity(target_block))
        target_block.timestamp = original_timestamp

        # 3. Attempt to modify previous hash
        print("\n3. Attempting to modify previous hash...")
        original_prev_hash = target_block.previous_hash
        target_block.previous_hash = "0" * 64
        print("Modified previous hash")
        print("Chain validity after modification:", blockchain.is_chain_valid())
        target_block.previous_hash = original_prev_hash

# Main Function

def main():
    # Create blockchain and miner
    blockchain = Blockchain()
    miner = Miner(difficulty=4)
    verifier = BlockchainVerifier()

    # Generate and add blocks
    print("\n=== Creating Test Blockchain ===")
    transactions1 = create_sample_transactions(4)
    transactions2 = create_sample_transactions(4)

    # Add blocks with mining
    block1 = Block(transactions1, blockchain.chain[-1].current_hash)
    block1.current_hash = miner.mine_block(block1)
    blockchain.chain.append(block1)

    block2 = Block(transactions2, blockchain.chain[-1].current_hash)
    block2.current_hash = miner.mine_block(block2)
    blockchain.chain.append(block2)

    # Verify blockchain integrity
    print("\n=== Initial Blockchain State ===")
    print("Chain valid:", blockchain.is_chain_valid())

    # Simulate attacks and verify integrity
    verifier.simulate_attack(blockchain)

    # Final verification
    print("\n=== Final Blockchain State ===")
    print("Chain valid:", blockchain.is_chain_valid())

if __name__ == "__main__":
    main()