# initiate API 

1. api call from perdix client
params: loan id, list of customer ids

2. store data to `aafi_request`

### Table **aafi_request**

id, customer-id, loan-id , fi-type[DEPOSIT|CREDIT_CARD],
consent-id, (all request params to have column), consent-url, consent-status,
session id, session-status, (other session fields)

3. call consent api & store req & response, consent-id, ...
4. take consent-URL & send notification by API
5. notification configurations, ....


# scheduler
if consent-id is NOT NULL & session-id is NULL
1. call consent GET API in scheduler interval until ACTIVE, till overall timeout (config based)
2. if ACTIVE, start data flow

# app startup
if session-id is NOT NULL & session-status != 'READY'
1. call ::Data Flow

# Session Flow (async) (analyse load later)
1. call /sessions/:consent-id
2. store session-id
3. write a callback to receive session READY status
4. call ::Data Flow

# Data Flow
1. call /session/:session-id
2. store to `aafi_details` table
3. update status in `aafi_request`

### Table **aafi_details**
id, session-id, response-json, parse-status, (other required fields)

# parse scheduler
1. for parse-status - PENDING
2. pull `aafi_details` table & parse json
3. pull FI type-wise objects & call FI-Type plugins


# FI-Type Plugin (DEPOSIT)
deal with child tables & ETL
- should be compressed tables

```sql
CREATE TABLE aafi_deposit (
    id INT PRIMARY KEY,
    type VARCHAR(50),
    masked_account_number VARCHAR(20),
    link_ref_number VARCHAR(20)
);

CREATE TABLE aafi_deposit_holder (
    id INT PRIMARY KEY,
    aafi_deposit_id INT,
    address VARCHAR(100),
    ckycCompliance VARCHAR(10),
    dob DATE,
    email VARCHAR(50),
    landline VARCHAR(20),
    mobile VARCHAR(20),
    name VARCHAR(50),
    nominee VARCHAR(20),
    pan VARCHAR(20),
    FOREIGN KEY (aafi_deposit_id) REFERENCES aafi_deposit(id)
);

CREATE TABLE aafi_deposit_summary (
    id INT PRIMARY KEY,
    aafi_deposit_id INT,
    balanceDateTime DATETIME,
    branch VARCHAR(50),
    currency VARCHAR(20),
    currentBalance DECIMAL(10,2),
    currentODLimit DECIMAL(10,2),
    drawingLimit DECIMAL(10,2),
    exchgeRate VARCHAR(20),
    facility VARCHAR(20),
    ifscCode VARCHAR(20),
    micrCode VARCHAR(20),
    openingDate DATE,
    pendingAmount DECIMAL(10,2),
    pendingTransactionType VARCHAR(20),
    status VARCHAR(20),
    type VARCHAR(20),
    FOREIGN KEY (aafi_deposit_id) REFERENCES aafi_deposit(id)
);

CREATE TABLE aafi_deposit_transaction (
    id INT PRIMARY KEY,
    aafi_deposit_id INT,
    amount DECIMAL(10,2),
    currentBalance DECIMAL(10,2),
    mode VARCHAR(20),
    narration VARCHAR(100),
    reference VARCHAR(20),
    transactionTimestamp DATETIME,
    txnId VARCHAR(20),
    type VARCHAR(20),
    valueDate DATE,
    FOREIGN KEY (aafi_deposit_id) REFERENCES aafi_deposit(id)
);
```
