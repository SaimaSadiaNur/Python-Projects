# quotes-data-pipeline
# Quotes Data Engineering Pipeline & REST API

A full-stack data pipeline built with Python that extracts web data, stores it in a normalized SQLite database, performs statistical EDA, and serves endpoints via an interactive REST API.

---

## Architecture Overview
[ Web Scraper ] ──> [ SQLite DB ] ──> [ Analytics / EDA ] ──> [ REST API ]
 (BeautifulSoup)     (Normalized)      (Pandas/Matplotlib)    (FastAPI)
