import matplotlib.pyplot as plt
import networkx as nx
from typing import List
import importlib.util
import os

# Get the absolute path to the blockchain file
blockchain_path = os.path.join(os.path.dirname(__file__), "group3_mini_blockchain.py")
spec = importlib.util.spec_from_file_location("blockchain", blockchain_path)
blockchain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blockchain)

# Now we can use the imported module
MerkleTree = blockchain.MerkleTree
Transaction = blockchain.Transaction
create_sample_transactions = blockchain.create_sample_transactions
Blockchain = blockchain.Blockchain

def visualize_merkle_tree(merkle_tree, filename="merkle_tree.png"):
    """Generate a visualization of the Merkle tree"""
    G = nx.DiGraph()
    
    def add_nodes(node, level=0, pos=0):
        if node is None:
            return
        
        # Add current node
        node_hash = node.hash  # MerkleNode has a hash attribute
        G.add_node(node_hash[:8], hash=node_hash[:8])
        
        if node.left:
            # Add left child
            left_hash = node.left.hash
            G.add_node(left_hash[:8], hash=left_hash[:8])
            G.add_edge(node_hash[:8], left_hash[:8])
            add_nodes(node.left, level + 1, pos - 1)
            
        if node.right:
            # Add right child
            right_hash = node.right.hash
            G.add_node(right_hash[:8], hash=right_hash[:8])
            G.add_edge(node_hash[:8], right_hash[:8])
            add_nodes(node.right, level + 1, pos + 1)
    
    # Build the graph
    add_nodes(merkle_tree.root)
    
    # Set up the plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=2000, font_size=8, font_weight='bold')
    
    # Save the plot
    plt.title("Merkle Tree Structure")
    plt.savefig(filename)
    plt.close()

def plot_mining_stats(mining_times: List[float], filename="mining_stats.png"):
    """Generate a bar plot of mining times"""
    plt.figure(figsize=(10, 6))
    
    # Create bar plot
    bars = plt.bar(range(1, len(mining_times) + 1), mining_times)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}s',
                ha='center', va='bottom')
    
    # Customize the plot
    plt.title('Block Mining Times')
    plt.xlabel('Block Number')
    plt.ylabel('Time (seconds)')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Save the plot
    plt.savefig(filename)
    plt.close()

def plot_blockchain_structure(blockchain, filename="blockchain_structure.png"):
    """Generate a visualization of the blockchain structure"""
    G = nx.DiGraph()
    
    # Add blocks as nodes
    for i, block in enumerate(blockchain.chain):
        block_hash = block.calculate_hash()
        # Access nonce directly from block
        nonce = getattr(block, 'nonce', 'N/A')
        block_info = f"Block {i}\nHash: {block_hash[:8]}...\nNonce: {nonce}"
        G.add_node(i, label=block_info)
        
        # Add edges between blocks
        if i > 0:
            G.add_edge(i-1, i)
    
    # Set up the plot
    plt.figure(figsize=(12, 6))
    pos = nx.spring_layout(G)
    
    # Draw the graph
    nx.draw(G, pos, node_color='lightgreen',
            node_size=3000, font_size=8, font_weight='bold')
    
    # Add labels
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Save the plot
    plt.title("Blockchain Structure")
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    # This script should be run after run_test.py
    # It will read the blockchain_test.log and generate visualizations
    print("Please run run_test.py first to generate the blockchain data.")
    print("Then run this script to generate visualizations.") 