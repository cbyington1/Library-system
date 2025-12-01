# Library Management System - Milestone 2
CS-4347 Database Systems

## Team Members
- Aliza Karim Karachiwalla
- Camden Scott Byington
- Eylul Guldik
- Jose Leonardo Del Rosario Dos Remedios
- Zahra Ashfaq

## Project Description
Library Management System implementing book search, loan management, borrower management, and fines processing with database schema.

## Language and Version
- **Language**: Python
- **Database**: PostgreSQL (hosted on Railway)

## Dependencies (Third Party Modules)
- psycopg2-binary (PostgreSQL adapter)

See `requirements.txt` for specific versions.

## Setup Instructions

### 1. Install Python

### 2. Create Virtual Environment

### 3. Activate Virtual Environment

### 4. Install Dependencies

### 5. Database Setup
The database is pre-configured and hosted on Railway PostgreSQL. Connection details are in `db_connection.py`.

To verify connection:
```bash
python db_connection.py
```

**Note**: Do NOT run `setup_db.py` unless you want to reset the database.

## Running the Application

Each feature can be tested individually:

### Book Search
```bash
python book_search.py
```
Searches for books by ISBN, title, or author 

### Book Loans
```bash
python book_loans.py
```
Handles checkout and checkin operations with validation 

### Borrower Management
```bash
python borrower_management.py
```
Creates new borrowers with auto-generated card numbers and duplicate SSN prevention.

### Fines
```bash
python fines.py
```
Calculates and updates fines at $0.25/day and processes payments.

## Project Structure
```
library-system/
├── db_connection.py          # Database connection helper
├── schema.sql                # Database schema 
├── setup_db.py               # Database setup script 
├── example_functions.py      # Example query patterns
├── book_search.py            # Feature 1: Book search
├── book_loans.py             # Feature 2: Checkout/checkin
├── borrower_management.py    # Feature 3: Borrower creation
├── fines.py                  # Feature 4: Fines calculation/payment
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Features Implemented

### 1. Book Search and Availability
- Single search field
- Case-insensitive substring matching
- Searches ISBN, title, and author names
- Returns: ISBN, title, authors , availability

### 2. Book Loans 
**Checkout:**
- Validates max 3 active loans per borrower
- Checks book availability
- Blocks checkout if borrower has unpaid fines
- Auto-sets due date to 14 days from checkout

**Checkin:**
- Search loans by ISBN, card number, or borrower name
- Updates date_in field

### 3. Borrower Management
- Creates new borrowers with all required fields
- Auto-generates card_no 
- Prevents duplicate SSN
- Validates required fields 

### 4. Fines 
- Calculates fines at $0.25/day
- Handles both returned late books and currently late books
- Updates existing unpaid fines
- Does not modify paid fines
- Payment processing:
  - Blocks payment for unreturned books
  - Requires full payment 
  - Groups fines by borrower

## Database Schema
- **BOOK**: isbn (PK), title
- **AUTHORS**: author_id (PK), name
- **BOOK_AUTHORS**: author_id (FK), isbn (FK)
- **BORROWER**: card_no (PK), ssn (UNIQUE), bname, address, phone
- **BOOK_LOANS**: loan_id (PK), isbn (FK), card_no (FK), date_out, due_date, date_in
- **FINES**: loan_id (PK, FK), fine_amt (DECIMAL), paid (BOOLEAN)

## Sample Data
Database includes:
- 30 books
- 30 authors
- 10 borrowers
- 14 book loans (mix of active, returned, on-time, late)
- 7 fines (paid and unpaid)