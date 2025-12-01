# borrower_management.py
from typing import Optional, List, Dict, Any
from db_connection import execute_query

def _normalize_ssn(ssn: str) -> str:
    """Ensure SSN is stored as 123-45-6789 if 9 digits are provided."""
    if ssn is None:
        return ssn
    digits = "".join(ch for ch in ssn if ch.isdigit())
    if len(digits) == 9:
        return f"{digits[0:3]}-{digits[3:5]}-{digits[5:9]}"
    return ssn.strip()

def _normalize_phone(phone: Optional[str]) -> Optional[str]:
    """Format 10-digit numbers as (123) 456-7890; otherwise keep as-is."""
    if not phone:
        return None
    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone.strip()

def create_borrower(ssn: str, name: str, address: str, phone: Optional[str] = None):
    """
    Create a new borrower.
    Returns:
      - int card_no on success
      - str error message on failure
    """
    try:
        if not ssn or not name or not address:
            return "Error: SSN, name, and address are required."

        ssn = _normalize_ssn(ssn)
        phone = _normalize_phone(phone)
        name = name.strip()
        address = address.strip()

        # 1) Duplicate SSN check
        existing = execute_query(
            "SELECT card_no FROM BORROWER WHERE ssn = %s;",
            (ssn,),
            fetch=True,
        )
        if existing:
            return "Error: A borrower with this SSN already exists."

        # 2) Insert and return generated card_no
        row = execute_query(
            """
            INSERT INTO BORROWER (ssn, bname, address, phone)
            VALUES (%s, %s, %s, %s)
            RETURNING card_no;
            """,
            (ssn, name, address, phone),
            fetch=True,
        )
        return row[0]["card_no"] if row else "Error: Borrower not created."
    except Exception as e:
        return f"Error creating borrower: {e}"

def find_borrowers(query: str) -> List[Dict[str, Any]]:
    """
    Search borrowers by exact card_no (if numeric) or substring match on ssn/bname (case-insensitive).
    """
    try:
        q = (query or "").strip()
        params = []
        clauses = []

        if q.isdigit():
            clauses.append("CAST(card_no AS TEXT) = %s")
            params.append(q)

        clauses.append("ssn ILIKE %s")
        params.append(f"%{q}%")

        clauses.append("bname ILIKE %s")
        params.append(f"%{q}%")

        sql = f"""
            SELECT card_no, ssn, bname, address, phone
            FROM BORROWER
            WHERE {" OR ".join(clauses)}
            ORDER BY card_no
            LIMIT 50;
        """
        return execute_query(sql, tuple(params), fetch=True)
    except Exception as e:
        return [{"error": f"Error searching borrowers: {e}"}]



