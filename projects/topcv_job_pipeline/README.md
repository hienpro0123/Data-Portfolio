# TopCV Job ETL Pipeline

This project is an automated **ETL pipeline** that crawls Data Analyst job postings from **TopCV**, cleans and standardizes key fields (salary, location, company), and loads the data into a **PostgreSQL** database for further analysis or dashboarding.

> 🧑‍💻 Built as a portfolio project to showcase web scraping, data cleaning, and basic data engineering skills (Python, Airflow, PostgreSQL, Docker).

---

## 1. Project Overview

- **Goal:** Build a simple, reproducible ETL pipeline that:
  - Extracts Data Analyst / Data-related jobs from TopCV.
  - Cleans messy salary strings and location text.
  - Avoids inserting duplicate job records.
  - Stores clean data in PostgreSQL, ready for analysis or BI tools.

- **Data source:**  
  Public job listings from [TopCV](https://www.topcv.vn/) (Data Analyst / Data Engineer / BI jobs).

- **Update frequency:**  
  Designed to run **daily** (or on-demand) to keep the job dataset up to date.

---

## 2. Architecture

High-level flow:

```text
            ┌───────────┐
            │  Airflow  │ (or Python scheduler)
            └─────┬─────┘
                  │
        ┌─────────▼─────────┐
        │   Extract (Python) │
        │  - requests        │
        │  - BeautifulSoup   │
        └─────────┬─────────┘
                  │ raw jobs (JSON/DataFrame)
        ┌─────────▼─────────┐
        │  Transform         │
        │  - clean salary    │
        │  - split city/dst  │
        │  - drop duplicates │
        └─────────┬─────────┘
                  │ clean data
        ┌─────────▼─────────┐
        │   Load (Postgres) │
        │   - upsert /      │
        │     insert only   │
        └───────────────────┘
