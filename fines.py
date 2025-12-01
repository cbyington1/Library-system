# fines.py
from datetime import date
from typing import List, Dict, Any
from db_connection import execute_query

DAILY_FINE = 0.25


def _calculate_fine(due_date, end_date) -> float:
    """Return fine amount based on days late × $0.25."""
    days_late = (end_date - due_date).days
    if days_late <= 0:
        return 0.00
    return round(days_late * DAILY_FINE, 2)


def update_fines() -> int:
    """
    Update or insert all fines based on late BOOK_LOANS records.
    Returns number of fines inserted or updated.
    """
    try:
        today = date.today()

        # Get all late loans (returned late OR currently late)
        loans = execute_query(
            """
            SELECT loan_id, due_date, date_in
            FROM BOOK_LOANS
            WHERE due_date < COALESCE(date_in, CURRENT_DATE);
            """,
            fetch=True
        )

        updates = 0

        for loan in loans:
            loan_id = loan["loan_id"]
            due = loan["due_date"]
            end_date = loan["date_in"] or today

            fine_amt = _calculate_fine(due, end_date)

            # Check if FINES row exists
            existing = execute_query(
                "SELECT fine_amt, paid FROM FINES WHERE loan_id = %s;",
                (loan_id,),
                fetch=True
            )

            if not existing:
                # INSERT new fine (unpaid)
                execute_query(
                    """
                    INSERT INTO FINES (loan_id, fine_amt, paid)
                    VALUES (%s, %s, FALSE);
                    """,
                    (loan_id, fine_amt),
                    fetch=False
                )
                updates += 1
            else:
                paid = existing[0]["paid"]
                old_amt = float(existing[0]["fine_amt"])

                if paid:
                    # Do not touch paid fines
                    continue

                if old_amt != fine_amt:
                    # UPDATE existing unpaid fine
                    execute_query(
                        """
                        UPDATE FINES
                        SET fine_amt = %s
                        WHERE loan_id = %s;
                        """,
                        (fine_amt, loan_id),
                        fetch=False
                    )
                    updates += 1

        return updates

    except Exception as e:
        return f"Error updating fines: {e}"


def get_fines_grouped(card_no: int, include_paid: bool = False) -> List[Dict[str, Any]]:
    """Return fines for a borrower grouped by loan_id."""
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
    """
    PAY all fines for a borrower.
    Cannot pay fines for books that are still checked out.
    Must pay full amount.
    Returns total amount paid or error.
    """
    try:
        # Get unpaid fines
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

        # Check for books not yet returned
        for row in unpaid:
            if row["date_in"] is None:
                return "Error: Cannot pay fines for books that are not yet returned."

        # Total amount to pay
        total = round(sum(float(row["fine_amt"]) for row in unpaid), 2)

        # Mark all unpaid fines as paid
        execute_query(
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
            (card_no,),
            fetch=False
        )

        return total

    except Exception as e:
        return f"Error processing payment: {e}"

if __name__ == "__main__":
    print("Updating fines...")
    print(update_fines())

    print("\nUnpaid fines for card_no = 3")
    print(get_fines_grouped(3))

    print("\nPaying fines for card_no = 3")
    print(pay_fines(3))

    print("\nFines after payment:")
    print(get_fines_grouped(3))
