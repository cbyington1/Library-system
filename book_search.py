from db_connection import get_db_connection


def search(search_term):
    """
    Search books by ISBN, title, or author name: case insensitive, substring

    Returns a list of dicts with:
        {
            "isbn": <str>,
            "title": <str>,
            "authors": <str>,        # comma separated
            "available": <bool>,     # True if not currently checked out
        }
    """
    print("DEBUG: running NEW search()")

    if search_term is None:
        search_term = ""
    search_term = search_term.strip()

    if not search_term:
        return []

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        pattern = f"%{search_term}%"

        query = """
            SELECT
                b.isbn,
                b.title,
                STRING_AGG(DISTINCT a.name, ', ') AS authors,
                CASE
                    WHEN MAX(
                        CASE
                            WHEN bl.date_in IS NULL AND bl.date_out IS NOT NULL
                                THEN 1
                            ELSE 0
                        END
                    ) = 1
                    THEN FALSE
                    ELSE TRUE
                END AS available
            FROM book AS b
            LEFT JOIN book_authors AS ba
                ON b.isbn = ba.isbn
            LEFT JOIN authors AS a
                ON ba.author_id = a.author_id
            LEFT JOIN book_loans AS bl
                ON b.isbn = bl.isbn
            WHERE
                b.isbn ILIKE %s
                OR b.title ILIKE %s
                OR a.name ILIKE %s
            GROUP BY
                b.isbn,
                b.title
            ORDER BY
                b.title;
        """

        cur.execute(query, (pattern, pattern, pattern))
        rows = cur.fetchall()
        conn.close()

        print("DEBUG: raw DB rows:", rows)

        results = []
        for row in rows:
            results.append({
                "isbn": row["isbn"],
                "title": row["title"],
                "authors": row["authors"] or "",
                "available": bool(row["available"]),
            })

        return results

    except Exception as e:
        return f"Error during search: {e}"


if __name__ == "__main__":
    print("DEBUG: running book_search.py as script")
    print(search("the"))
