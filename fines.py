from datetime import date
from typing import List, Dict, Any
from db_connection import execute_query, get_db_connection

DAILY_FINE = 0.25

def _calculate_fine(due_date, end_date) -> float:
    days_late = (end_date - due_date).days
    if days_late <= 0:
        return 0.00
    return round(days_late * DAILY_FINE, 2)

def update_fines() -> int:
    try:
        today = date.today()

        loans = execute_query(
            """
            SELECT loan_id, due_date, date_in
            FROM BOOK_LOANS
            WHERE due_date < COALESCE(date_in, CURRENT_DATE);
            """,
            fetch=True
        )

        conn = get_db_connection()
        cursor = conn.cursor()
        updates = 0

        for loan in loans:
            loan_id = loan["loan_id"]
            due = loan["due_date"]
            end_date = loan["date_in"] or today

            fine_amt = _calculate_fine(due, end_date)

            existing = execute_query(
                "SELECT fine_amt, paid FROM FINES WHERE loan_id = %s;",
                (loan_id,),
                fetch=True
            )

            if not existing:
                cursor.execute(
                    """
                    INSERT INTO FINES (loan_id, fine_amt, paid)
                    VALUES (%s, %s, FALSE);
                    """,
                    (loan_id, fine_amt)
                )
                updates += 1
            else:
                paid = existing[0]["paid"]
                old_amt = float(existing[0]["fine_amt"])

                if paid:
                    continue

                if old_amt != fine_amt:
                    cursor.execute(
                        """
                        UPDATE FINES
                        SET fine_amt = %s
                        WHERE loan_id = %s;
                        """,
                        (fine_amt, loan_id)
                    )
                    updates += 1

        conn.commit()
        conn.close()
        return updates

    except Exception as e:
        return f"Error updating fines: {e}"

def get_fines_grouped(card_no: int, include_paid: bool = False) -> List[Dict[str, Any]]:
    try:
        clauses = ["bl.card_no = %s"]
        params = [card_no]

        if not include_paid:
            clauses.append("f.paid = FALSE")

        sql = f"""
            SELECT
                f.loan_id,
                f.fine_amt,
                f.paid,
                bl.isbn,
                bl.date_out,
                bl.due_date,
                bl.date_in
            FROM FINES f
            JOIN BOOK_LOANS bl ON f.loan_id = bl.loan_id
            WHERE {" AND ".join(clauses)}
            ORDER BY f.loan_id;
        """

        return execute_query(sql, tuple(params), fetch=True)

    except Exception as e:
        return [{"error": f"Error retrieving fines: {e}"}]

def pay_fines(card_no: int):
    try:
        unpaid = execute_query(
            """
            SELECT f.loan_id, f.fine_amt, bl.date_in
            FROM FINES f
            JOIN BOOK_LOANS bl ON f.loan_id = bl.loan_id
            WHERE bl.card_no = %s AND f.paid = FALSE;
            """,
            (card_no,),
            fetch=True
        )

        if not unpaid:
            return "No unpaid fines for this borrower."

        for row in unpaid:
            if row["date_in"] is None:
                return "Error: Cannot pay fines for books that are not yet returned."

        total = round(sum(float(row["fine_amt"]) for row in unpaid), 2)

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE FINES
            SET paid = TRUE
            WHERE loan_id IN (
                SELECT f.loan_id
                FROM FINES f
                JOIN BOOK_LOANS bl ON f.loan_id = bl.loan_id
                WHERE bl.card_no = %s AND f.paid = FALSE
            );
            """,
            (card_no,)
        )
        
        conn.commit()
        conn.close()

        return total

    except Exception as e:
        return f"Error processing payment: {e}"

if __name__ == "__main__":
    print("Testing fines...\n")
    
    print("1. Update fines:")
    result = update_fines()
    print(f"   Updated {result} fines")
    
    print("\n2. Get unpaid fines for card_no = 2:")
    fines = get_fines_grouped(2)
    print(f"   Found {len(fines)} unpaid fines")
    for f in fines:
        print(f"   - Loan {f['loan_id']}: ${f['fine_amt']}")
    
    print("\n3. Pay fines for card_no = 2:")
    result = pay_fines(2)
    print(f"   Result: {result}")