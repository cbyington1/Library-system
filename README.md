# Library Management System - Milestone 2

Database backend for library system. Milestone 3 will add Flask and frontend.

## Setup

1. Clone repo
2. Activate virtual environment:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database setup (creates tables + sample data):
```bash
python setup_db.py
```

5. Test connection:
```bash
python db_connection.py
```

## Database

- **Platform**: Railway PostgreSQL
- **Connection**: Managed in `db_connection.py`
- **Tables**: BOOK, AUTHORS, BOOK_AUTHORS, BORROWER, BOOK_LOANS, FINES
- **Sample Data**: 30 books, 30 authors, 10 borrowers

## Features to Implement

Each feature should be a standalone function that takes parameters and returns results. This makes it easy to call from Flask later.

### 1. book_search.py
```python
def search(search_term):
    # Search ISBN, title, or author
    # Return list of dicts with: isbn, title, authors, availability
    pass
```

### 2. book_loans.py
```python
def checkout(isbn, card_no):
    # Check out book
    # Return loan_id on success, error message on failure
    pass

def checkin(loan_ids):
    # Check in books
    # Return count of books checked in
    pass
```

### 3. borrower_management.py
```python
def create_borrower(ssn, name, address, phone=None):
    # Create new borrower
    # Return card_no on success, error message on failure
    pass
```

### 4. fines.py
```python
def calculate_fines():
    # Update fines for all late books ($0.25/day)
    # Return count of fines updated
    pass

def pay_fines(card_no):
    # Pay all fines for borrower
    # Return total paid on success, error message on failure
    pass
```

## How to Build Your Feature

1. Open your file (e.g., `book_search.py`)
2. Import connection:
```python
from db_connection import get_db_connection
```

3. Write your function:
```python
def your_function(params):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Your SQL query here
    query = "SELECT ..."
    cursor.execute(query, (params,))
    results = cursor.fetchall()
    
    conn.close()
    return results
```

4. Test it:
```python
if __name__ == "__main__":
    result = your_function(test_params)
    print(result)
```

See `example_functions.py` for query patterns

## Guidelines for Integration (Milestone 3)

Structure your functions so they're easy to call from routes:

```python
def search(search_term):
    # Does one thing, returns clean data
    return [{"isbn": "...", "title": "...", "authors": "...", "available": True}]
```

**Key points:**
- Take parameters as function arguments (not input())
- Return data 
- Return dicts/lists that can be converted to JSON
- Handle errors with try/except, return error messages as strings

## Requirements

From project PDF:
- Book Search: Case-insensitive substring matching on ISBN/title/author
- Checkout: Max 3 loans per borrower, check availability, check unpaid fines, due date = 14 days
- Checkin: Update date_in field
- Borrower: Auto-generate card_no, prevent duplicate SSN
- Fines: $0.25/day, can't pay until books returned, must pay all at once
