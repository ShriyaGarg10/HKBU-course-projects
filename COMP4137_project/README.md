# Mini Blockchain System

## 1. Artifact Identification

**Title:** Mini Blockchain System

**Group Number:** 3

**Group Members:**
- Ahmed Ahtasham (22229817)
- Chen Boyu (22240985)
- Shriya GARG (24512028)

**Abstract:**
This project aims to create a simple blockchain system in Python that can do several things, including showing you the core features of a blockchain system in a modular, educational way. The transaction generation part, along with the Merkle tree construction using SHA-256 hashing and blockchain implementation with the help of proof-of-work mining, is part of the system. It contributes to a robust transaction verification system, a secure block construction via cryptographic hashing, and comprehensive integrity checks for attack vectors of different types. It is implemented based on the linear, modular pipeline architecture from user account creation to a fully functional blockchain with attack detection capabilities. This artifact is a reproducible reference implementation that fits the experimental results and security analyses mentioned in the final project report.

## 2. Artifact Dependencies and Requirements

### Hardware Requirements
- Minimum CPU: 1.6 GHz processor
- Minimum RAM: 4 GB
- Minimum Disk Space: 500 MB

### Operating System Requirements
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

### Programming Language and Libraries
- Python 3.11+
- cryptography (42.0.5+)
- hashlib (built-in)
- datetime (built-in)
- typing (built-in)

### Input Dataset Information
Using the `create_sample_transactions()` function, the transactions are generated at runtime
- Sample transactions include:
  - Alice → Bob: 100 units
  - Bob → Charlie: 50 units
  - Charlie → Dave: 75 units
  - Dave → Alice: 25 units
  - Additional transactions as needed

### Other Dependencies
- No additional dependencies required
- No virtual environment necessary
- No need of any external CLI tools

## 3. Artifact Installation and Deployment Process

### Step 1: Download/Clone the Project
```bash
git clone [repository-url]
cd [repository-directory]
```

### Step 2: Install Dependencies
```bash
pip install cryptography matplotlib networkx
```

### Step 3: Test the applications and generate visualization
```bash
# Execute automated test pipeline
python run_test.py
```

Note: The visualization files will be automatically generated when running run_test.py. You don't need to run visualization.py separately as it's already integrated into the test pipeline.

### Additional Tools
The project includes two additional Python scripts:

1. **run_test.py**
   - Automated test pipeline that runs the complete blockchain process
   - Generates detailed logs in `blockchain_test.log`
   - Tests account creation, transaction generation, Merkle tree construction, and mining
   - Includes attack simulation and integrity verification
   - Automatically generates visualizations:
     - Merkle Tree Structure (`merkle_tree.png`)
     - Mining Statistics (`mining_stats.png`)
     - Blockchain Structure (`blockchain_structure.png`)

2. **visualization.py**
   - Contains visualization functions used by run_test.py
   - Not meant to be run separately
   - If run directly, it will prompt to run run_test.py first

### Estimated Time Requirements
- Installation: 2-3 minutes
- First run: 1-2 minutes
- Full system execution: 3-5 minutes
- Visualization generation: 1-2 minutes

## 4. Reproducibility of Experiments

### Experimental Process
When executed, the program performs the following sequence:

1. **Account and Key Generation**
   - Creates RSA key pairs (2048-bit)
   - Generates blockchain addresses from public keys

2. **Transaction Generation**
   - Creates SISO (Single-Input-Single-Output) transactions
   - Signs transactions using RSA private keys
   - Generates transaction IDs (TIDs) using SHA-256

3. **Merkle Tree Construction**
   - Builds binary Merkle tree from transaction hashes
   - Computes root hash through pairwise hashing
   - Supports transaction inclusion verification

4. **Block Construction and Mining**
   - Creates block headers with:
     - Previous block hash
     - Merkle root
     - Timestamp
     - Nonce
   - Performs proof-of-work mining (difficulty: 4 leading zeros)
   - Links blocks through hash pointers

5. **Integrity Verification**
   - Validates transaction signatures
   - Verifies Merkle tree proofs
   - Checks block hash integrity
   - Validates chain continuity

### Expected Output
The program produces the following outputs:

1. **Transaction Processing**
   ```
   === Building Merkle Tree ===
   Leaf nodes:
   Leaf 0: [transaction-hash]
   Leaf 1: [transaction-hash]
   ...
   ```

2. **Mining Results**
   ```
   Mining block with difficulty 4...
   Block mined! Nonce: [value], Hash: 0000[hash]
   ```

3. **Attack Simulation**
   ```
   === Simulating Blockchain Attacks ===
   1. Attempting to modify transaction amount...
   Merkle root verification failed!
   Integrity check after modification: False
   ```

### Time Estimates
- Full system execution: 3-5 minutes
- Individual block mining: 1-2 minutes
- Attack simulation: 30-60 seconds

### Alignment with Project Report
The outcome structure and experimental test findings match the figures and analytical sections in the final project document. The system demonstrates:
- Transaction generation and verification
- Merkle tree construction and validation
- Proof-of-work mining with difficulty 4
- Attack detection and prevention
- Chain integrity maintenance

The final implementation is a reference that reproduces all security assessments and experimental outcomes mentioned in the project report. 