import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://postgres:zXkZqqJnxmArUdzYEbeTAeEXmRvBkSgy@yamanote.proxy.rlwy.net:43976/railway"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def execute_query(query, params=None, fetch=True):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, params or ())
        
        if fetch:
            results = cursor.fetchall()
            conn.close()
            return results
        else:
            conn.commit()
            conn.close()
            return None
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

if __name__ == "__main__":
    try:
        conn = get_db_connection()
        print("Database connection successed")
        conn.close()
    except Exception as e:
        print(f" Database connection failed: {e}")