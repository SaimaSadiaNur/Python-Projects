# Quotes Data Engineering Pipeline: End-to-End ETL & REST API
# Executive Summary
This project demonstrates an end-to-end data pipeline designed to automate the extraction, normalization, storage, analysis, and API delivery of web-based quote data.

In many content management, market research, and media applications, unstructured text data must be parsed, structured, and made programmatically accessible across services. This project solves that workflow challenge by taking raw HTML text from web sources, processing it through an automated ETL (Extract, Transform, Load) pipeline into a relational database, generating analytics visual reports, and hosting a production-ready REST API for real-time data consumption.

# Business & Data Problem
Unstructured data scattered across the web cannot be efficiently queried, filtered, or integrated into downstream analytics dashboards and software applications. To make this data actionable, the system required:

Automated extraction of raw quotes, author metadata, and categorical tags.

Relational database modeling with standardized schemas to ensure data integrity.

Automated programmatic data visualization for immediate analytics reporting.

A production-grade web API to serve structured JSON data with low latency to external clients and front-end blogs.

# Architecture & Technical Approach
+-------------------+      +---------------------+      +---------------------+
|  Web Source Data  | ---> | Python Scraper/ETL  | ---> |   SQLite Database   |
| (Quotes & Metadata)|     | (BeautifulSoup/Pandas)|    | (Relational Schema) |
+-------------------+      +---------------------+      +---------------------+
                                                                   |
                                                                   v
                           +---------------------+      +---------------------+
                           | Analytics & Reports | <--- |   FastAPI REST API  |
                           |  (Matplotlib Data)  |      |  (Render Cloud App) |
                           +---------------------+      +---------------------+
# 1. Data Extraction & ETL (BeautifulSoup / Pandas)
Extracted unstructured quote records, author names, and associate tags.

Cleaned and parsed raw text into structured Pandas DataFrames.

Exported clean data artifacts for analytical processing.

# 2. Relational Database Design (SQLite3)
Modeled a database schema separating quotes and authors to eliminate data redundancy.

Utilized primary and foreign key constraints (author_id) to optimize join queries.

# 3. Data Analysis & Insights (Matplotlib / Pandas)
Computed distributions of top tags and author frequency.

Programmatically generated analytical charts (top_tags.png) saved directly to the /reports directory for executive review.

# 4. Cloud API Deployment (FastAPI / Uvicorn / Render)
Developed queryable REST API endpoints supporting custom tag filtering, author search, and pagination limits.

Implemented dynamic absolute pathing (Path(__file__)) for cloud compatibility.

Deployed the web service to Render, exposing live Swagger UI documentation and production JSON endpoints.

# Results & Deliverables
# Live Interactive API Documentation (Swagger UI): https://quotes-pipeline-api.onrender.com/docs

# Live Production Endpoint: https://quotes-pipeline-api.onrender.com/quotes?limit=5

# API Sample Output (GET /quotes?limit=5):

JSON
{
  "count": 5,
  "data": [
    {
      "id": 1,
      "quote": "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”",
      "author": "Albert Einstein",
      "tags": ["change", "deep-thoughts", "thinking", "world"]
    },
    {
      "id": 2,
      "quote": "“It is our choices, Harry, that show what we truly are, far more than our abilities.”",
      "author": "J.K. Rowling",
      "tags": ["abilities", "choices"]
    }
  ]
}
# Visual Reports & Analytics
# Tag Distribution Analytics:
<img width="3000" height="1500" alt="top_tags" src="https://github.com/user-attachments/assets/ab3441e8-4cdd-472c-a908-6d250d8e7def" />
# Interactive Documentation (Swagger UI):
<img width="939" height="366" alt="api-docs-screenshot" src="https://github.com/user-attachments/assets/63b3be99-8146-4854-a23b-48fdf3033614" />
.

# Repository Structure
# Plaintext
Web-Scraping-Quote-Pipeline/
│
├── data/
│   └── quotes.db               # SQLite Relational Database
├── reports/
│   ├── top_tags.png            # Generated Analytics Chart
│   └── quotes_table.html       # Interactive Static HTML Export
├── src/
│   ├── scraper.py              # ETL Scraper Module
│   ├── database.py             # SQLite Schema Setup & Load Script
│   ├── eda.py                  # Analytical Visualization Script
│   └── api.py                  # FastAPI REST Service Module
├── requirements.txt            # Project Dependencies
└── README.md                   # Project Documentation & Case Study
# How to Run Locally
# 1. Prerequisites
Ensure you have Python 3.9+ installed on your machine.

# 2. Setup Environment
# Bash
# Clone repository
git clone https://github.com/SaimaSadiaNur/Python-Projects.git
cd Python-Projects/Web-Scraping-Quote-Pipeline

# Install dependencies
pip install -r requirements.txt
3. Run the API Locally
Bash
uvicorn src.api:app --reload
Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your web browser to test endpoints locally.

# Limitations & Future Enhancements
Database Scaling: The current deployment uses an embedded SQLite database suitable for read-heavy static datasets. Migrating to PostgreSQL would improve concurrent write handling and scalability under high traffic.

Scraper Automation: Pipeline execution is currently run on-demand. Implementing an automated cron schedule (e.g., via GitHub Actions or Airflow) would keep database records synced automatically with external updates.
