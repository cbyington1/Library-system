from db_connection import get_db_connection

def example_select():
    """SELECT query"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM AUTHORS LIMIT 5"
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    return results

def example_where():
    """WHERE clause"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM BOOK WHERE isbn = %s"
    cursor.execute(query, ("9780141439518",))
    result = cursor.fetchone()
    
    conn.close()
    return result

def example_join():
    """JOIN tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT b.title, a.name
        FROM BOOK b
        JOIN BOOK_AUTHORS ba ON b.isbn = ba.isbn
        JOIN AUTHORS a ON ba.author_id = a.author_id
        LIMIT 5
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    return results

def example_insert():
    """INSERT record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO AUTHORS (name) VALUES (%s) RETURNING author_id"
    cursor.execute(query, ("Example Author",))
    new_id = cursor.fetchone()['author_id']
    
    conn.commit()
    conn.close()
    
    return new_id

def example_update():
    """UPDATE record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "UPDATE AUTHORS SET name = %s WHERE author_id = %s"
    cursor.execute(query, ("Updated Name", 31))
    
    conn.commit()
    conn.close()

def example_count():
    """COUNT records"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT COUNT(*) as total FROM BOOK"
    cursor.execute(query)
    result = cursor.fetchone()
    
    conn.close()
    return result['total']

def example_error_handling():
    """Error handling"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT * FROM BOOK WHERE isbn = %s"
        cursor.execute(query, ("9780141439518",))
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        conn.close()
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing database connection...\n")
    
    print("SELECT:")
    authors = example_select()
    print(f"Found {len(authors)} authors")
    
    print("\nWHERE:")
    book = example_where()
    print(f"Found: {book['title']}")
    
    print("\nJOIN:")
    results = example_join()
    print(f"Found {len(results)} results")
    
    print("\nCOUNT:")
    total = example_count()
    print(f"Total books: {total}")
    
    print("\nDone!")