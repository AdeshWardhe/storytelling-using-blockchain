# 📖 Blockchain-Based Collaborative Storytelling Platform

A decentralized storytelling platform that combines collaborative writing, community voting, blockchain technology, and Ethereum smart contracts to create a transparent and immutable storytelling experience.

Users can contribute story segments, vote on proposed continuations, and permanently record finalized story chapters using a custom blockchain integrated with the Ethereum Sepolia Test Network.

---

## 🚀 Project Overview

Traditional collaborative storytelling platforms rely on centralized databases where content can be modified, deleted, or controlled by a single authority.

This project introduces a blockchain-powered approach where approved story contributions are secured using cryptographic hashing, Proof-of-Work mining, and Ethereum smart contracts, ensuring transparency, traceability, and integrity of story evolution.

The platform enables multiple users to collaboratively build a story while maintaining a verifiable history of every finalized contribution.

---

## ✨ Features

* 📚 Collaborative story creation
* 🗳️ Community voting system
* ⚡ Real-time updates using Flask-SocketIO
* ⛏️ Proof-of-Work blockchain mining
* 🔐 SHA-256 cryptographic hashing
* ⛓️ Custom blockchain implementation
* 🌐 Ethereum Sepolia smart contract integration
* 🔍 Public transaction verification
* 📜 Immutable story history

---

## 🎯 Problem Statement

Collaborative storytelling platforms often depend on centralized databases where content can be modified or removed without transparency.

This project solves these challenges by:

* Preserving story history permanently
* Preventing unauthorized modifications
* Providing transparent validation
* Enabling community-driven story progression
* Maintaining verifiable records using blockchain technology

---

## 🏗️ System Architecture

```text
┌───────────────────────┐
│         Users         │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│   Flask Web Interface │
│    HTML/CSS/JS        │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│   Flask-SocketIO      │
│  Real-Time Updates    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Candidate Submission  │
│     & Voting Layer    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Story Finalization    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  Blockchain Engine    │
│ SHA-256 + PoW Mining  │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Ethereum Smart        │
│ Contract (Sepolia)    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Transaction Proof     │
│ Verification          │
└───────────────────────┘
```

---

## 🔄 Workflow

### 1. Story Submission

Users submit story continuations through the web interface.

### 2. Candidate Creation

Submitted entries are stored as candidate story segments.

### 3. Voting

Community members vote for their preferred continuation.

### 4. Story Finalization

The highest-voted contribution is selected.

### 5. Block Generation

A blockchain block is created containing:

* Block Index
* Story Content
* Author
* Timestamp
* Previous Hash
* Nonce

### 6. Mining

Proof-of-Work mining is performed until a valid hash is generated.

### 7. Blockchain Update

The mined block is appended to the blockchain.

### 8. Ethereum Storage

The block proof is recorded on a Solidity smart contract deployed on the Ethereum Sepolia Test Network.

### 9. Verification

Users can verify transaction records through Ethereum explorers.

---

## 🧱 Block Structure

```json
{
  "index": 1,
  "timestamp": "2025-06-01",
  "author": "User",
  "content": "Story segment",
  "previous_hash": "a4b7c8...",
  "nonce": 2456,
  "hash": "0000abc123..."
}
```

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask
* Flask-SocketIO

### Frontend

* HTML
* CSS
* JavaScript

### Blockchain

* Custom Blockchain Implementation
* SHA-256 Hashing
* Proof-of-Work Mining

### Ethereum

* Solidity
* Web3.py
* MetaMask
* Sepolia Testnet

### Development Tools

* Git
* GitHub
* Remix IDE
* Etherscan

---

## 📂 Project Structure

```text
storytelling-using-blockchain/
│
├── app.py
├── helper.py
├── state_module_2.py
├── requirements.txt
├── .env.example
│
├── templates/
│   ├── index.html
│   ├── second.html
│   └── welcome.html
│
├── test_5.py
├── test_helper.py
├── test_submit.py
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/AdeshWardhe/storytelling-using-blockchain.git
cd storytelling-using-blockchain
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SEPOLIA_RPC_URL=your_rpc_url
PRIVATE_KEY=your_private_key
CONTRACT_ADDRESS=your_contract_address
```

### Run Application

```bash
python app.py
```

---

This project was developed for educational and research purposes to explore the integration of blockchain technology with collaborative content creation systems.
