# Orion Backend

“Orion Backend — Built with clarity, powered by intelligence.” 🌌

This repository contains the backend for the **Orion AI-Powered Financial Control Hub**. It is a modular, production-ready API built with Python, FastAPI, and PostgreSQL.

## ⚙️ Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic for migrations
- **Authentication**: JWT (PyJWT) with role-based access
- **Configuration**: Pydantic Settings

## 🧩 Architecture

The backend is designed as a **Modular Monolith**. Each business domain (e.g., `auth`, `transactions`) is encapsulated in its own module under `app/modules/`, promoting separation of concerns and maintainability.

```
orion-backend/
│
├── app/
│   ├── core/         # Core components (config, db, security)
│   ├── modules/      # Business logic modules
│   ├── main.py       # FastAPI app entrypoint
│   └── dependencies.py # Shared dependencies
│
├── alembic/          # Database migrations
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variable template
└── README.md         # This file
```

## 🚀 Getting Started Locally

### Prerequisites

- Python 3.11+ installed.
- PostgreSQL running on your local machine.
- A tool to create a database (e.g., `psql` or a GUI like DBeaver/PgAdmin).

### 1. Clone the Repository

Clone this project to your local machine and navigate into the `orion-backend` directory.

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```sh
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all required Python packages from `requirements.txt`.

```sh
pip install -r requirements.txt
```

### 4. Set Up the Database

- Make sure your local PostgreSQL server is running.
- Create a new database named `orion`.
- Create a user `admin` with password `admin` and grant it permissions to the `orion` database.

### 5. Set Up Environment Variables

Create a `.env` file in the `orion-backend/` directory by copying the example file.

```sh
cp .env.example .env
```

The `DATABASE_URL` should already be configured for `localhost`. Open the `.env` file and change the `JWT_SECRET_KEY` to a strong, unique secret. You can generate one using:
```sh
openssl rand -hex 32
```

### 6. Run the Application

From the `orion-backend/` directory, run the application using Uvicorn:

```sh
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 7. Access the API Documentation

Once the application is running, you can access the interactive API documentation (powered by Swagger UI) at:

[http://localhost:8000/docs](http://localhost:8000/docs)

## 🧭 API Overview

- `/api/v1/auth/register`: Create a new user.
- `/api/v1/auth/login`: Authenticate and receive a JWT token.
- `/api/v1/transactions/`: Create or retrieve transactions for the logged-in user.
- `/api/v1/ai/insights`: (Placeholder) Get AI-driven insights.
- `/api/v1/analytics/overview`: (Placeholder) Get financial analytics.