# Design and Implementation of an Educational Cryptocurrency Blockchain System

This project is a Master's Thesis focused on bridging the gap between theoretical blockchain concepts and practical engineering skills. It provides a modular, "glass-box" educational blockchain ecosystem consisting of a production-like Python backend, a Vue.js visualization explorer, and a 5-module laboratory curriculum.

## Project Structure

The repository is divided into two primary sections:

### 1. [Thesis](./thesis/)
Contains the LaTeX source code for the Master's Thesis document.
- **Chapters:** Cover theoretical frameworks (DLT, Cryptography, Consensus), system design, technical implementation, and the educational curriculum.
- **Figures:** UML diagrams, architecture maps, and screenshots of the finalized system.
- **Bibliography:** Comprehensive references for blockchain research.

### 2. [Practical Part](./practical-part/)
The technical implementation and educational materials.
- **[Final System](./practical-part/final_system/pos-blockchain/):** The complete software artifact.
    - **Blockchain Backend:** A Python-based P2P node using FastAPI, Keccak-256 hashing, and ECDSA signatures. It defaults to a Proof of Stake (PoS) consensus mechanism.
    - **Blockchain Explorer:** A Vue.js frontend that visualizes block propagation, the mempool, validators, and transaction history in real-time.
    - **Orchestration:** Docker Compose configurations to simulate a distributed network of nodes on a single machine.
- **[Educational Modules](./practical-part/modules/):** Five progressive laboratory exercises, each containing `starter` code for students and `solution` code for reference.
    - **Module 1:** Network Fundamentals (Hard Forking & P2P Discovery).
    - **Module 2:** Consensus Mechanisms (Implementing Proof of Work).
    - **Module 3:** Performance Analysis (TPS Benchmarking & Stress Testing).
    - **Module 4:** Application Layer (Digital Assets & Library Management System).
    - **Module 5:** System Extensibility (Hybrid On-chain/Off-chain Storage).

## Technical Stack

- **Backend:** Python 3.11, FastAPI, Uvicorn, `p2pnetwork`, `eth-keys`.
- **Frontend:** Vue.js 2, Webpack, `vue-resource`.
- **Infrastructure:** Docker, Docker Compose.
- **Cryptography:** Keccak-256 (Hashing), SECP256k1 (ECDSA).

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for running scripts outside Docker)
- Node.js (for local explorer development)

### Running the Final System
1. Navigate to the system directory:
   ```bash
   cd practical-part/final_system/pos-blockchain/
   ```
2. Start the blockchain network (4 nodes):
   ```bash
   docker-compose up --build
   ```
3. Start the Blockchain Explorer:
   ```bash
   cd explorer
   npm install
   npm run dev
   ```
4. Access the Explorer at `http://localhost:8080`.

## License
This project is developed as part of a Master's Thesis at the University of South Bohemia and the Deggendorf Institute of Technology. And part of the POS Implementation was inspired by this [POS implementation](https://github.com/rafrasenberg/proof-of-stake-blockchain) by Raf Rasenberg