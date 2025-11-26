import psycopg2
from datetime import datetime, timedelta

DATABASE_URL = "postgresql://postgres:zXkZqqJnxmArUdzYEbeTAeEXmRvBkSgy@yamanote.proxy.rlwy.net:43976/railway"

def setup_database():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("Setting up Library Management System database...")
    
    print("\nCreating tables...")
    with open('schema.sql', 'r') as f:
        schema = f.read()
        cursor.execute(schema)
    conn.commit()
    print("Tables created")
    
    print("\nAdding sample authors...")
    authors = [
        ("William Shakespeare",), ("Jane Austen",), ("Charles Dickens",),
        ("Mark Twain",), ("Ernest Hemingway",), ("F. Scott Fitzgerald",),
        ("George Orwell",), ("J.K. Rowling",), ("Stephen King",),
        ("Agatha Christie",), ("Leo Tolstoy",), ("Virginia Woolf",),
        ("James Baldwin",), ("Toni Morrison",), ("Gabriel Garcia Marquez",),
        ("Harper Lee",), ("J.R.R. Tolkien",), ("Isaac Asimov",),
        ("Ray Bradbury",), ("Margaret Atwood",), ("Kurt Vonnegut",),
        ("Maya Angelou",), ("Oscar Wilde",), ("Emily Dickinson",),
        ("Edgar Allan Poe",), ("Herman Melville",), ("Fyodor Dostoevsky",),
        ("Homer",), ("Dante Alighieri",), ("Miguel de Cervantes",),
    ]
    
    cursor.executemany("INSERT INTO AUTHORS (name) VALUES (%s)", authors)
    conn.commit()
    print(f"Added {len(authors)} authors")
    
    print("\nAdding sample books...")
    books = [
        ("9780141439518", "Pride and Prejudice"),
        ("9780743273565", "The Great Gatsby"),
        ("9780141439600", "Great Expectations"),
        ("9780451524935", "1984"),
        ("9780590353427", "Harry Potter and the Sorcerer's Stone"),
        ("9780385472579", "The Shining"),
        ("9780062315007", "And Then There Were None"),
        ("9780743477116", "Adventures of Huckleberry Finn"),
        ("9780684801223", "The Old Man and the Sea"),
        ("9780156907392", "To the Lighthouse"),
        ("9780679783268", "Love in the Time of Cholera"),
        ("9780679410034", "Anna Karenina"),
        ("9780679732761", "The Fire Next Time"),
        ("9781400033416", "Beloved"),
        ("9780141182605", "Hamlet"),
        ("9780061120084", "To Kill a Mockingbird"),
        ("9780547928227", "The Hobbit"),
        ("9780553293357", "Foundation"),
        ("9781451673319", "Fahrenheit 451"),
        ("9780385490818", "The Handmaid's Tale"),
        ("9780385333849", "Slaughterhouse-Five"),
        ("9780345391803", "I Know Why the Caged Bird Sings"),
        ("9780141439730", "The Picture of Dorian Gray"),
        ("9780316769174", "The Catcher in the Rye"),
        ("9780743297332", "Moby-Dick"),
        ("9780374528379", "Crime and Punishment"),
        ("9780140449389", "The Odyssey"),
        ("9780142437223", "The Divine Comedy"),
        ("9780060934347", "Don Quixote"),
        ("9780141187761", "Wuthering Heights"),
    ]
    
    cursor.executemany("INSERT INTO BOOK (isbn, title) VALUES (%s, %s)", books)
    conn.commit()
    print(f"Added {len(books)} books")
    
    print("\nLinking books to authors...")
    book_authors = [
        (2, "9780141439518"), (6, "9780743273565"), (3, "9780141439600"),
        (7, "9780451524935"), (8, "9780590353427"), (9, "9780385472579"),
        (10, "9780062315007"), (4, "9780743477116"), (5, "9780684801223"),
        (12, "9780156907392"), (15, "9780679783268"), (11, "9780679410034"),
        (13, "9780679732761"), (14, "9781400033416"), (1, "9780141182605"),
        (16, "9780061120084"), (17, "9780547928227"), (18, "9780553293357"),
        (19, "9781451673319"), (20, "9780385490818"), (21, "9780385333849"),
        (22, "9780345391803"), (23, "9780141439730"), (1, "9780316769174"),
        (26, "9780743297332"), (27, "9780374528379"), (28, "9780140449389"),
        (29, "9780142437223"), (30, "9780060934347"), (2, "9780141187761"),
    ]
    
    cursor.executemany("INSERT INTO BOOK_AUTHORS (author_id, isbn) VALUES (%s, %s)", book_authors)
    conn.commit()
    print(f"Linked {len(book_authors)} books to authors")
    
    print("\nAdding sample borrowers...")
    borrowers = [
        ("123-45-6789", "John Smith", "123 Main St, Dallas, TX 75001", "214-555-0001"),
        ("234-56-7890", "Mary Johnson", "456 Oak Ave, Richardson, TX 75080", "972-555-0002"),
        ("345-67-8901", "Robert Williams", "789 Elm St, Plano, TX 75023", "469-555-0003"),
        ("456-78-9012", "Patricia Brown", "321 Pine Rd, Frisco, TX 75034", "214-555-0004"),
        ("567-89-0123", "Michael Davis", "654 Cedar Ln, Allen, TX 75013", "972-555-0005"),
        ("678-90-1234", "Jennifer Garcia", "987 Maple Dr, McKinney, TX 75070", "469-555-0006"),
        ("789-01-2345", "William Rodriguez", "147 Birch Ct, Garland, TX 75040", "214-555-0007"),
        ("890-12-3456", "Elizabeth Martinez", "258 Spruce Way, Irving, TX 75061", "972-555-0008"),
        ("901-23-4567", "David Anderson", "369 Willow Ln, Carrollton, TX 75006", "469-555-0009"),
        ("012-34-5678", "Sarah Taylor", "741 Ash Blvd, Addison, TX 75001", "214-555-0010"),
    ]
    
    cursor.executemany("INSERT INTO BORROWER (ssn, bname, address, phone) VALUES (%s, %s, %s, %s)", borrowers)
    conn.commit()
    print(f"Added {len(borrowers)} borrowers")
    
    print("\nAdding sample book loans...")
    today = datetime.now().date()
    
    loans = [
        ("9780141439518", 1, today - timedelta(days=5), today + timedelta(days=9), None),
        ("9780547928227", 3, today - timedelta(days=3), today + timedelta(days=11), None),
        ("9780385490818", 5, today - timedelta(days=7), today + timedelta(days=7), None),
        ("9780743273565", 2, today - timedelta(days=20), today - timedelta(days=6), None),
        ("9780451524935", 4, today - timedelta(days=25), today - timedelta(days=11), None),
        ("9781451673319", 6, today - timedelta(days=18), today - timedelta(days=4), None),
        ("9780141439600", 1, today - timedelta(days=30), today - timedelta(days=16), today - timedelta(days=18)),
        ("9780590353427", 7, today - timedelta(days=25), today - timedelta(days=11), today - timedelta(days=12)),
        ("9780679410034", 8, today - timedelta(days=40), today - timedelta(days=26), today - timedelta(days=27)),
        ("9780547928227", 9, today - timedelta(days=35), today - timedelta(days=21), today - timedelta(days=22)),
        ("9780385472579", 2, today - timedelta(days=40), today - timedelta(days=26), today - timedelta(days=20)),
        ("9780062315007", 10, today - timedelta(days=35), today - timedelta(days=21), today - timedelta(days=18)),
        ("9780679783268", 3, today - timedelta(days=50), today - timedelta(days=36), today - timedelta(days=30)),
        ("9780141182605", 5, today - timedelta(days=45), today - timedelta(days=31), today - timedelta(days=28)),
    ]
    
    cursor.executemany("INSERT INTO BOOK_LOANS (isbn, card_no, date_out, due_date, date_in) VALUES (%s, %s, %s, %s, %s)", loans)
    conn.commit()
    print(f"Added {len(loans)} book loans")
    
    print("\nAdding sample fines...")
    fines = [
        (11, 1.50, True), (12, 0.75, False), (13, 1.50, False),
        (14, 0.75, True), (4, 1.50, False), (5, 2.75, False), (6, 1.00, False),
    ]
    
    cursor.executemany("INSERT INTO FINES (loan_id, fine_amt, paid) VALUES (%s, %s, %s)", fines)
    conn.commit()
    print(f"Added {len(fines)} fines")
    
    print("\nDatabase setup complete!")
    print("\nSummary:")
    cursor.execute("SELECT COUNT(*) FROM AUTHORS")
    print(f"Authors: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM BOOK")
    print(f"Books: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM BORROWER")
    print(f"Borrowers: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM BOOK_LOANS")
    print(f"Book Loans: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM FINES")
    print(f"Fines: {cursor.fetchone()[0]}")
    
    conn.close()

if __name__ == "__main__":
    try:
        setup_database()
    except Exception as e:
        print(f"\nError setting up database: {e}")
        raise