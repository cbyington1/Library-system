from typing import Optional, List, Dict, Any
from db_connection import execute_query, get_db_connection

def _normalize_ssn(ssn: str) -> str:
    if ssn is None:
        return ssn
    digits = "".join(ch for ch in ssn if ch.isdigit())
    if len(digits) == 9:
        return f"{digits[0:3]}-{digits[3:5]}-{digits[5:9]}"
    return ssn.strip()

def _normalize_phone(phone: Optional[str]) -> Optional[str]:
    if not phone:
        return None
    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone.strip()

def create_borrower(ssn: str, name: str, address: str, phone: Optional[str] = None):
    try:
        if not ssn or not name or not address:
            return "Error: SSN, name, and address are required."

        ssn = _normalize_ssn(ssn)
        phone = _normalize_phone(phone)
        name = name.strip()
        address = address.strip()

        existing = execute_query(
            "SELECT card_no FROM BORROWER WHERE ssn = %s;",
            (ssn,),
            fetch=True,
        )
        if existing:
            return "Error: A borrower with this SSN already exists."

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO BORROWER (ssn, bname, address, phone)
            VALUES (%s, %s, %s, %s)
            RETURNING card_no;
            """,
            (ssn, name, address, phone)
        )
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        
        return row["card_no"] if row else "Error: Borrower not created."
    except Exception as e:
        return f"Error creating borrower: {e}"

def find_borrowers(query: str) -> List[Dict[str, Any]]:
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

if __name__ == "__main__":
    print("Testing borrower management...\n")
    
    print("1. Create new borrower:")
    result = create_borrower("999887777", "Test Person", "123 Test St", "2145551234")
    print(f"   Result: {result}")
    
    print("\n2. Try duplicate SSN:")
    result = create_borrower("123-45-6789", "Duplicate", "456 Fake St")
    print(f"   Result: {result}")
    
    print("\n3. Find borrowers with 'Smith':")
    results = find_borrowers("Smith")
    print(f"   Found {len(results)} borrowers")
    for r in results:
        print(f"   - {r['bname']} (Card: {r['card_no']})")