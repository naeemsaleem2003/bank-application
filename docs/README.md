# Bank Application

A simple banking system for learning backend architecture and service-layer business rules.

## Live Demo

**[Open the deployed Dinero bank application](https://66pqkdw2m8.execute-api.us-east-1.amazonaws.com/)**

The application is hosted on AWS through API Gateway and Lambda. To test it:

1. Create a profile with a name, email address, and password.
2. Sign in and open a checking or savings account.
3. Make a deposit or withdrawal.
4. Confirm the balance and transaction history update.

Use test information only. Do not enter real banking details or reuse an important
password. Developers can also explore the deployed
**[API documentation](https://66pqkdw2m8.execute-api.us-east-1.amazonaws.com/docs)**.

## Features

- Register and log in
- Create an account
- View account details
- Deposit money
- Withdraw money
- View transaction history

## Current Implementation

This full-stack application uses a React/Vite frontend, FastAPI backend, JWT
authentication, MongoDB persistence, and an AWS Lambda deployment.

- AccountRepository reads and writes account data in MongoDB
- UserRepository reads and writes user data in MongoDB
- TransactionRepository reads and writes transaction data in MongoDB
- TransactionService contains deposit and withdraw validation and business logic

## Project Structure

```
models/
    account.py
    user.py
    transaction.py

repositories/
    AccountRepository.py
    UserRepository.py
    TransactionRepository.py
    mongo.py

services/
    account_service.py
    auth_service.py
    transaction_service.py

frontend/
    src/

BankAPI.py
Dockerfile
requirements.txt
```

## Architecture

1. API layer receives request
2. Service layer applies business rules
3. Repository layer stores and retrieves data
4. Model layer defines data objects

## Business Rules

- Deposit amount must be a valid positive number
- Withdraw amount must be a valid positive number
- Cannot withdraw more than current account balance
- Every successful deposit and withdraw creates a transaction record

## Quick Start

### Prerequisites

- Python 3
- Node.js 18 or newer
- A MongoDB Atlas database or compatible MongoDB instance

### 1. Create and activate a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB

Create a `.env` file in the repository root:

```dotenv
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>/
JWT_SECRET_KEY=<a-random-secret-with-at-least-32-characters>
```

Replace both placeholders with your own development values. The application uses
the `bank_application` database and never requires real customer information.

### 4. Run the API

```bash
python -m uvicorn BankAPI:app --reload
```

The interactive local API documentation is available at
`http://127.0.0.1:8000/docs`.

### 5. Run the frontend

In a second terminal:

```bash
cd frontend
cp .env.example .env.local
npm ci
npm run dev
```

Open `http://localhost:5173` and follow the same test flow described under
**Live Demo**.

### 6. Run the MongoDB smoke test

After configuring `.env`, run the smoke test from the project root:

```bash
python scripts/mongodb_smoke_test.py
```

The test connects to the configured database and leaves behind one uniquely named
sample user, one checking account, a deposit, and a withdrawal. It verifies that
the final balance is `100.25` and that both transaction records can be read back.

You can inspect the resulting entries in MongoDB Atlas under
**Database > Browse Collections**.

## Verification

Run the backend unit tests from the repository root:

```bash
python -m unittest discover -s tests
```

Validate the frontend from `frontend/`:

```bash
npm run lint
npm run build
```

## API Endpoints

### Auth

- POST /auth/register
- POST /auth/token
- GET /auth/me

### Accounts

- GET /accounts
- GET /accounts/{account_id}
- POST /accounts

### Transactions

- POST /accounts/{account_id}/deposit
- POST /accounts/{account_id}/withdraw
- GET /accounts/{account_id}/transactions

## Team Notes

- Keep repository classes focused on data access only
- Keep service classes focused on validation and business logic only
- Keep credentials in environment variables and do not commit `.env`
