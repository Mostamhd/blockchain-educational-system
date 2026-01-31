### **Master's Thesis Structure**

#### **Chapter 1: Introduction**
* **1.1 Background:** The rise of Blockchain technology and the widening skills gap in engineering education.
* **1.2 Problem Statement:** The lack of "Glass-Box" educational tools for understanding distributed systems internals.
* **1.3 Research Objectives:** To design and implement a modular, Python-based blockchain system and a corresponding laboratory curriculum.
* **1.4 Thesis Structure:** Roadmap of the document.

#### **Chapter 2: Theoretical Framework**
* **2.1 Distributed Ledger Technology (DLT):** Blockchain architecture, block headers, and bodies.
* **2.2 Cryptographic Primitives:** Hash functions (SHA-256) and Digital Signatures (ECDSA).
* **2.3 Security Risks and Attack Vectors:** Double-spending, Sybil attacks, and 51% Majority attacks.
* **2.4 Consensus Algorithms:** Deep dive into Proof of Work (PoW), Proof of Stake (PoS), Delegated Proof of Stake (DPoS), and Proof of History (PoH).
* **2.5 Related Work:** Case studies of Bitcoin (UTXO/PoW), Ethereum (Account/PoS), and Solana (PoH/Pipelining).
* **2.6 Comparative Analysis:** The Blockchain Trilemma and technical comparison table.
* **2.7 Summary**

#### **Chapter 3: System Analysis and Design**
* **3.1 Requirement Analysis:** Functional requirements (P2P syncing, Consensus swapping) and Non-functional requirements (Modularity, Dockerization).
* **3.2 System Architecture:** High-level Layered Architecture (Network Layer, Consensus Layer, Application Layer).
* **3.3 Detailed Component Design:** UML Class Diagrams (Node composition) and Transaction Lifecycle Flowcharts.
* **3.4 Technology Stack Justification:** Justification for Python (readability) and Docker (network simulation).
* **3.5 Summary**

#### **Chapter 4: Technical Implementation**
*(This chapter details the engineering of the underlying software artifact)*
* **4.1 Core Data Structures:** Implementation of Block, Transaction, and Blockchain classes.
* **4.2 Networking Layer:** Implementation of the P2P socket handler, message broadcasting, and node discovery.
* **4.3 Consensus Engine:** Implementation of the Strategy Pattern for runtime consensus swapping.
* **4.4 API and Visualization:** Development of the FastAPI endpoints and the Blockchain Explorer frontend.
* **4.5 Summary**

#### **Chapter 5: Educational Curriculum Design**
* **5.1 Approach and Methodology:** Constructionist Learning theory and Problem-Based Learning (PBL).
* **5.2 Repository Structure:** Explanation of the scaffolding approach (Starter vs. Solution directories).
* **5.3 Module 1: Network Fundamentals:** Bootstrapping, Genesis Forking, and Docker Orchestration.
* **5.4 Module 2: Consensus Mechanisms:** Implementing Proof of Work to mitigate Sybil attacks.
* **5.5 Module 3: Performance Analysis:** System instrumentation, benchmarking TPS, and stress testing.
* **5.6 Module 4: Application Layer and Smart Assets:** Building the "Library Management System" (Event Sourcing).
* **5.7 Module 5: System Extensibility:** Architectural design challenge (Hybrid On-chain/Off-chain storage).
* **5.8 Summary**

#### **Chapter 6: Results and Discussion**
* **6.1 Introduction:** Overview of the dual-phase evaluation strategy.
* **6.2 Phase I: Technical System Evaluation:**
    * Experimental Setup (Hardware/Network).
    * Throughput Analysis (PoS vs. PoW comparison).
    * Latency and Resource Utilization (CPU bottlenecks).
* **6.3 Phase II: Curriculum Validation:**
    * Pilot Study Methodology.
    * Functional Completion Results (Sample outputs/screenshots).
    * Participant Feedback (Qualitative assessment).
* **6.4 Discussion:** Synthesis of technical validity and educational utility.
* **6.5 Limitations:** Sample size, prototype constraints, and simplified cryptography.
* **6.6 Summary**

#### **Chapter 7: Conclusion and Future Work**
* **7.1 Summary of Contributions:** Recap of the software artifact and the 5-module curriculum.
* **7.2 Future Work:** Transitioning to high-performance languages (Rust/Go), implementing Kademlia DHT for discovery, and expanding the curriculum to Smart Contracts (Solidity).



---

### **Local Compilation (Docker)**

This project is configured to be compiled locally using Docker, avoiding the need to install a massive LaTeX distribution on your host machine. It uses `xelatex` and `latexmk` for automated builds with support for Noto Naskh Arabic fonts.

#### **Option 1: VS Code (Recommended)**
1.  Install the **LaTeX Workshop** extension.
2.  Open `thesis/main.tex`.
3.  Use the `Docker Compose: latexmk` recipe (via `Cmd+Opt+B` or the LaTeX sidebar).
4.  The extension will automatically build the container and compile your PDF.

#### **Option 2: Terminal**
1.  Navigate to the `thesis/` directory.
2.  Run the following command:
    ```bash
    docker-compose run --rm compiler
    ```
3.  The resulting `main.pdf` will be available in the `build/` directory.

### **Cleaning Up**
Since all output goes to `build/`, you can simply delete that folder to clean up.


---