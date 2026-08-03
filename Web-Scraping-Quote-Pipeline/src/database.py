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

print(f" Database schema initialized at: {db_path}")


def insert_quotes(quotes_data: list[dict], db_path: Path = DB_PATH) -> None:
    """Inserts scraped quote dictionaries into the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    inserted_count = 0

    for item in quotes_data:
        author_name = item["author"]
        quote_text = item["quote"]
        # Convert tag list to JSON string for SQLite storage
        tags_json = json.dumps(item.get("tags", []))

        # 1. Insert or ignore author to get author_id
        cursor.execute(
            "INSERT OR IGNORE INTO authors (name) VALUES (?)",
            (author_name,)
        )
        
        cursor.execute(
            "SELECT author_id FROM authors WHERE name = ?",
            (author_name,)
        )
        author_id = cursor.fetchone()[0]

        # 2. Insert quote associated with author_id
        try:
            cursor.execute(
                """
                INSERT INTO quotes (author_id, quote_text, tags)
                VALUES (?, ?, ?)
                """,
                (author_id, quote_text, tags_json)
            )
            inserted_count += 1
        except sqlite3.IntegrityError:
            # Skip duplicate quote text
            pass

    conn.commit()
    conn.close()
    print(f" Successfully inserted {inserted_count} quotes into SQLite!\n")
                   
if __name__ == "__main__":
    init_db()

