from src.database import init_db, insert_quotes
from src.scraper import scrape_all_quotes


def run_pipeline():
    print("========================================")
    print("  STARTING QUOTES DATA PIPELINE")
    print("========================================\n")

    # Step 1: Initialize DB
    init_db()

    # Step 2: Scrape web data
    quotes = scrape_all_quotes()

    # Step 3: Insert into SQLite
    if quotes:
        insert_quotes(quotes)
        print(" ETL Pipeline execution completed successfully!")
    else:
        print(" No data scraped. Pipeline aborted.")


if __name__ == "__main__":
    run_pipeline()
