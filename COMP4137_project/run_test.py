import sys
import logging
from datetime import datetime
from typing import List
import matplotlib.pyplot as plt
import networkx as nx
import importlib.util
import os
import json


blockchain_path = os.path.join(os.path.dirname(__file__), "group3_mini_blockchain.py")
spec = importlib.util.spec_from_file_location("blockchain", blockchain_path)
blockchain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blockchain)


Account = blockchain.Account
Transaction = blockchain.Transaction
MerkleTree = blockchain.MerkleTree
Block = blockchain.Block
Blockchain = blockchain.Blockchain
create_sample_transactions = blockchain.create_sample_transactions
BlockchainVerifier = blockchain.BlockchainVerifier


from visualization import visualize_merkle_tree, plot_mining_stats, plot_blockchain_structure


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('blockchain_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_blockchain_test():
    """Run the complete blockchain test pipeline"""
    logging.info("=== Starting Blockchain Test Pipeline ===")
    mining_times = []
    

    logging.info("\n1. Creating Test Accounts")
    alice = Account("Alice")
    bob = Account("Bob")
    charlie = Account("Charlie")
    dave = Account("Dave")
    
    logging.info(f"Alice's address: {alice.get_address()[:10]}...")
    logging.info(f"Bob's address: {bob.get_address()[:10]}...")
    logging.info(f"Charlie's address: {charlie.get_address()[:10]}...")
    logging.info(f"Dave's address: {dave.get_address()[:10]}...")
    

    logging.info("\n2. Creating Sample Transactions")
    transactions = create_sample_transactions(4)
    for i, tx in enumerate(transactions):
        logging.info(f"Transaction {i}: {tx.sender[:10]}... → {tx.receiver[:10]}... ({tx.amount} units)")
    

    logging.info("\n3. Building Merkle Tree")
    merkle_tree = MerkleTree(transactions)
    logging.info(f"Merkle Root: {merkle_tree.get_root_hash()}")
    

    visualize_merkle_tree(merkle_tree)
    

    logging.info("\n4. Creating and Mining Blocks")
    blockchain = Blockchain()
    

    logging.info("\nMining Block 1...")
    start_time = datetime.now()
    blockchain.add_block(transactions)
    mining_time = (datetime.now() - start_time).total_seconds()
    mining_times.append(mining_time)
    logging.info(f"Block 1 mined in {mining_time:.2f} seconds")
    

    logging.info("\nMining Block 2...")
    start_time = datetime.now()
    blockchain.add_block(transactions)
    mining_time = (datetime.now() - start_time).total_seconds()
    mining_times.append(mining_time)
    logging.info(f"Block 2 mined in {mining_time:.2f} seconds")
    

    plot_mining_stats(mining_times)
    

    logging.info("\n5. Verifying Blockchain Integrity")
    is_valid = blockchain.is_chain_valid()
    logging.info(f"Blockchain is valid: {is_valid}")
    

    plot_blockchain_structure(blockchain)
    

    logging.info("\n6. Simulating Attacks")
    BlockchainVerifier.simulate_attack(blockchain)
    
    logging.info("\n=== Test Pipeline Completed ===")
    return blockchain, merkle_tree, mining_times

if __name__ == "__main__":
    blockchain, merkle_tree, mining_times = run_blockchain_test() 