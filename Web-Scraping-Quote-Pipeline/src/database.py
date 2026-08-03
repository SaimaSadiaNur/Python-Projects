from pathlib import Path
import sqlite3

def init_db(db_path ="data/quotes.db" ):
    folder = Path("data/")
    folder.mkdir(parents = True, exist_ok = True)

    connection = sqlite3.connect("data/quotes.db")
    cursor = connection.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        create table IF NOT EXISTS author (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT UNIQUE NOT NULL           
        )
    """)
    cursor.execute("""
        create table IF NOT EXISTS quotes (
            quote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            quote_text TEXT UNIQUE NOT NULL,
            tags TEXT,
            FOREIGN KEY (author_id) REFERENCES author(author_id)
        )

    """)
    connection.commit()
    connection.close()
    print("Database and tables initialized successfully!")
                   
if __name__ == "__main__":
    init_db()

