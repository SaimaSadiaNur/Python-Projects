import json
import sqlite3
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Quotes API")
DB_PATH = Path("data/quotes.db")


def get_db_connection():
    if not DB_PATH.exists():
        raise HTTPException(
            status_code=500, detail="Database file not found."
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Quotes Data Pipeline API!",
    }


@app.get("/quotes")
def get_quotes(
    tag: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT q.quote_id, q.quote_text, q.tags, a.name AS author_name
        FROM quotes q
        JOIN authors a ON q.author_id = a.author_id
        WHERE 1=1
    """
    params = []
    if author:
        query += " AND a.name LIKE ?"
        params.append(f"%{author}%")
    if tag:
        query += " AND q.tags LIKE ?"
        params.append(f"%{tag}%")

    query += " LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = [
        {
            "id": r["quote_id"],
            "quote": r["quote_text"],
            "author": r["author_name"],
            "tags": json.loads(r["tags"]) if r["tags"] else [],
        }
        for r in rows
    ]
    return {"count": len(results), "data": results}