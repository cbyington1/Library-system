# book_loans.py
from datetime import datetime, timedelta
from db_connection import get_db_connection

# --------------------------------------------------------
# Helper: count active loans for borrower
# --------------------------------------------------------
def borrower_active_loans(card_no):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS count
        FROM book_loans
        WHERE card_no = %s
          AND date_in IS NULL;
    """, (card_no,))

    row = cur.fetchone()
    conn.close()
    return row['count']

# --------------------------------------------------------
# Helper: check unpaid fines
# --------------------------------------------------------
def borrower_unpaid_fines(card_no):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS count
        FROM fines f
        JOIN book_loans bl ON f.loan_id = bl.loan_id
        WHERE bl.card_no = %s
          AND f.paid = FALSE
          AND f.fine_amt > 0;
    """, (card_no,))

    row = cur.fetchone()
    conn.close()
    return row['count']

# --------------------------------------------------------
# Helper: check if a book is already checked out
# --------------------------------------------------------
def book_is_checked_out(isbn):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS count
        FROM book_loans
        WHERE isbn = %s
          AND date_in IS NULL;
    """, (isbn,))

    row = cur.fetchone()
    conn.close()
    return row['count'] > 0

# --------------------------------------------------------
# CHECKOUT
# --------------------------------------------------------
def checkout(isbn, card_no):
    # Borrower cannot exceed 3 active loans
    if borrower_active_loans(card_no) >= 3:
        return "ERROR: Borrower already has 3 active loans."

    # Borrower cannot have unpaid fines
    if borrower_unpaid_fines(card_no) > 0:
        return "ERROR: Borrower has unpaid fines."

    # Book must be available
    if book_is_checked_out(isbn):
        return "ERROR: Book is already checked out."

    conn = get_db_connection()
    cur = conn.cursor()

    today = datetime.now().date()
    due_date = today + timedelta(days=14)

    cur.execute("""
        INSERT INTO book_loans (isbn, card_no, date_out, due_date, date_in)
        VALUES (%s, %s, %s, %s, NULL)
        RETURNING loan_id;
    """, (isbn, card_no, today, due_date))

    loan_id = cur.fetchone()['loan_id']
    conn.commit()
    conn.close()

    return f"SUCCESS: Book checked out. Loan ID: {loan_id}"

# --------------------------------------------------------
# FIND ACTIVE LOANS
# --------------------------------------------------------
def find_loans(isbn=None, card_no=None, name=None):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT bl.loan_id, bl.isbn, b.title, bl.card_no, br.bname,
               bl.date_out, bl.due_date
        FROM book_loans bl
        JOIN book b ON bl.isbn = b.isbn
        JOIN borrower br ON bl.card_no = br.card_no
        WHERE bl.date_in IS NULL
    """

    params = []

    if isbn:
        query += " AND bl.isbn = %s"
        params.append(isbn)

    if card_no:
        query += " AND bl.card_no = %s"
        params.append(card_no)

    if name:
        query += " AND LOWER(br.bname) LIKE %s"
        params.append(f"%{name.lower()}%")

    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()

    return results

# --------------------------------------------------------
# CHECKIN
# --------------------------------------------------------
def checkin(loan_id):
    conn = get_db_connection()
    cur = conn.cursor()

    today = datetime.now().date()

    cur.execute("""
        UPDATE book_loans
        SET date_in = %s
        WHERE loan_id = %s;
    """, (today, loan_id))

    conn.commit()
    conn.close()

    return "SUCCESS: Book checked in."
