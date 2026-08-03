import json
import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Define paths relative to the project structure
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "quotes.db"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


def run_eda(db_path: Path = DB_PATH) -> None:
    """Reads quotes data from SQLite, performs exploratory data analysis using Pandas,

    and exports summary visual charts to the reports/ directory.
    """
    if not db_path.exists():
        print(f" Database not found at {db_path}. Please run main.py first.")
        return

    # 1. Connect to SQLite and load data with SQL JOIN
    conn = sqlite3.connect(db_path)

    query = """
        SELECT 
            q.quote_id,
            q.quote_text,
            q.tags,
            a.name AS author_name
        FROM quotes q
        JOIN author a ON q.author_id = a.author_id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f" Loaded {len(df)} rows from SQLite database.\n")

    # 2. Data Cleaning: Convert JSON string tags into actual Python lists
    df["tags_list"] = df["tags"].apply(lambda x: json.loads(x) if x else [])

    # 3. Analyze Top Authors
    author_counts = df["author_name"].value_counts()
    print("---  TOP 5 AUTHORS BY QUOTE COUNT ---")
    print(author_counts.head(5).to_string())
    print("\n")

    # 4. Analyze Top Tags using Pandas explode()
    df_tags = df.explode("tags_list")
    tag_counts = df_tags["tags_list"].value_counts().dropna()

    print("---  TOP 10 MOST COMMON TAGS ---")
    print(tag_counts.head(10).to_string())
    print("\n")

    # 5. Generate and Save Chart
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    top_10_tags = tag_counts.head(10)

    # Seaborn styling
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(
        x=top_10_tags.values,
        y=top_10_tags.index,
        palette="Blues_r",
        hue=top_10_tags.index,
        legend=False,
    )

    plt.title("Top 10 Most Popular Quote Tags", fontsize=14, fontweight="bold")
    plt.xlabel("Number of Quotes", fontsize=12)
    plt.ylabel("Tag Name", fontsize=12)
    plt.tight_layout()

    output_path = REPORTS_DIR / "top_tags.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"📈 Chart successfully saved to: {output_path}")


if __name__ == "__main__":
    run_eda()
