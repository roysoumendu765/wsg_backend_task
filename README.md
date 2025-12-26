# 🚀 Transaction Webhook Service (Backend)

A production-ready **FastAPI** service that ingests transaction webhooks, ensures **idempotent processing**, persists data to **PostgreSQL**, and asynchronously processes transactions in the background.

This service is designed to handle real-world webhook challenges such as **duplicate delivery**, **async workflows**, and **fault tolerance**.

---

## 🧩 Tech Stack

- **Python 3.11+**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy (Async)**
- **asyncpg**
- **Uvicorn**
- **Docker & Docker Compose**

---

## 📁 Project Structure

```bash
backend/
├── app/
│ ├── main.py # FastAPI entrypoint
│ ├── database.py # Async DB connection
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ ├── crud.py # Database operations
│ ├── worker.py # Background processing
│
├── create_tables.py # Database bootstrap script
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Run Locally

## Environment Variables

Create a `.env` file inside the `backend/` directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:<password>@localhost:5433/webhooks_db
```

## Local Postgresql Setup:

```bash
psql -h localhost -p 5433 -U postgres
CREATE DATABASE webhooks_db;
```

## Create Tables: (Run Once in the terminal):

```bash
python create_tables.py
```

## Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start the Server

```bash
uvicorn app.main:app --reload
```

## API Endpoints

- GET / 

```bash
Response
{
  "status": "HEALTHY",
  "current_time": "2025-12-27T03:10:00Z"
}
```

- POST /v1/webhooks/transactions

```bash
Payload
{
  "transaction_id": "tx_12345",
  "source_account": "PNB",
  "destination_account": "SBI",
  "amount": 100,
  "currency": "USD"
}
```

- GET /v1/transactions/{transaction_id}

## Docker Support

```bash
docker-compose up --build
```




