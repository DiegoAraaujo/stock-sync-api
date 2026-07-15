# Stock Sync API

A REST API in Python for stock and order management, featuring a synchronization (webhook) endpoint that simulates integration between an e-commerce/mobile app and an external ERP system.

## About the project

This is a study project focused on consolidating backend concepts in Python — specifically REST APIs, data persistence, and system integration patterns (webhooks). The stack and domain (inventory, orders, retail) were chosen to reflect common scenarios in retail back-office systems.

My main experience is in Node.js/NestJS and TypeScript. This project was built to apply the same architectural principles I already use day to day — layer separation, data validation, automated testing — using Python and FastAPI instead.

## Stack

- **FastAPI** — web framework for building the API
- **SQLAlchemy** — ORM for data modeling and database access
- **PostgreSQL** — relational database
- **Pydantic** — input/output schema validation
- **Pytest** — automated testing
- **Docker & Docker Compose** — containerization and local orchestration

## Features

### Products

- Full CRUD (create, list, retrieve, update, delete)
- Direct stock update (simulates a manual adjustment made by a store employee)

### Orders

- Order creation with automatic stock deduction
- Insufficient stock validation before confirming an order
- Guarantees stock is not changed when an order fails

### Stock synchronization (Webhook)

- Endpoint that simulates receiving stock updates from an external system (ERP)
- Every update is recorded in a sync log, marked as success or failure
- The endpoint never returns an error to the calling system — even when the product doesn't exist, the failure is logged internally for later review, without breaking the integration
- Log query endpoint, with a filter for failures only

## Why a webhook?

In a real-world scenario, stock is usually controlled by an existing system (an ERP, for example), while a separate application (a mobile app or e-commerce platform) needs to stay in sync with those changes. Instead of that application repeatedly polling the ERP to check if something changed, the ERP itself notifies the application the moment a change happens, via an HTTP call to a predefined endpoint.

This project simulates that flow: the `/webhooks/stock` endpoint represents the receiving side of that notification. Since there is no real ERP integrated, calls are simulated manually for testing and demonstration purposes.

## Architecture

The project follows a feature-based structure, with clear separation between layers:

```
app/
├── products/       # Product domain
│   ├── router.py   # HTTP routes
│   ├── service.py  # Business logic
│   ├── models.py   # Data model (SQLAlchemy)
│   └── schemas.py  # Input/output validation (Pydantic)
├── orders/         # Order domain
├── sync/           # Webhook and sync logs
├── database.py     # Database connection setup
└── main.py         # Application entry point
tests/              # Automated tests (one file per domain)
```

Each domain is self-contained and follows the same pattern, which keeps the project easy to maintain and extend.

## How to run

### Prerequisites

- Python 3.12+
- PostgreSQL installed and running locally

### Steps

1. Clone the repository and enter the folder:

```bash
git clone https://github.com/YOUR-USERNAME/stock-sync-api.git
cd stock-sync-api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database named `stock_sync`.

5. Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env    # Linux/Mac
copy .env.example .env  # Windows
```

Edit the generated `.env` with your PostgreSQL connection string.

6. Run the application:

```bash
uvicorn app.main:app --reload
```

7. Access the interactive API docs at:

```
http://127.0.0.1:8000/docs
```

## Running with Docker

As an alternative to the manual setup above, the project can be run fully containerized, without installing PostgreSQL locally.

1. Create a `.env.docker` file in the project root:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/stock_sync
```

2. Build and start the containers:

```bash
docker compose up --build
```

3. Access the interactive API docs at:

```bash
http://127.0.0.1:8000/docs
```

This spins up two containers: the API and a PostgreSQL instance, already connected to each other.

### Running tests

```bash
pytest -v
```

## Possible improvements

- Use Alembic for migration versioning, instead of automatic table creation
- Authentication and authorization on routes
- Real integration with an ERP (e.g. Odoo, via XML-RPC or REST API)
