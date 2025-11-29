# 🚀 PostgreSQL Data Engineering Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)

A production-grade **ETL (Extract, Transform, Load)** pipeline that ingests live data from the NewsAPI, processes it using Pandas, and warehouses it in a PostgreSQL database.

The entire stack is containerized using **Docker Compose** with built-in health checks and network isolation.

---

## 🏗 Architecture
1.  **Extract:** Fetches raw JSON data from the [NewsAPI](https://newsapi.org/) (Tech Headlines).
2.  **Transform:** Cleans data, handles missing values, and standardizes schema using `Pandas`.
3.  **Load:** Inserts data into a `PostgreSQL` database using `SQLAlchemy`.
4.  **Orchestrate:** Managed via `Docker Compose` to ensure the database is healthy before the pipeline runs.

---

## ⚡ Key Features
* **Containerization:** Fully isolated environment using Docker.
* **Resilience:** Implements `healthcheck` in Docker Compose to prevent race conditions (waiting for DB to be ready).
* **Security:** Uses `.env` files to manage sensitive credentials (no hardcoded passwords).
* **Type Safety:** Uses strict schema validation before loading.

---

## 🛠 Project Structure
```bash
├── main.py              # The core ETL script
├── Dockerfile           # Python environment definition
├── docker-compose.yml   # Multi-container orchestration (App + DB)
├── requirements.txt     # Locked dependencies
└── .env.example         # Security template (Copy this to .env)
