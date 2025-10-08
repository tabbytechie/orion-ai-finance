# Orion Backend API 💻

> "Built with clarity, powered by intelligence." 🌌

![GitHub](https://img.shields.io/github/license/yourusername/orion-ai-finance)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-4169E1?logo=postgresql&logoColor=white)

This repository contains the backend for the **Orion AI-Powered Financial Control Hub**. It's a high-performance, modular API built with Python, FastAPI, and PostgreSQL, designed for secure and scalable financial data management.

## 💡 Key Features

- 💰 **Full CRUD for Transactions**: Securely create, read, update, and delete financial transactions.
- 🔑 **Robust JWT Authentication**: Secure user registration and login with role-based access control and password hashing.
- 📊 **Placeholder Analytics Endpoints**: Defined API contracts for future financial overview and trend analysis.
- 🤖 **Placeholder AI Integration**: Defined API contracts for future AI-powered insights.
- 📦 **Modular Architecture**: Clean separation of concerns with modules for each business domain.
- 📝 **Comprehensive API Documentation**: Auto-generated, interactive API docs via Swagger UI and ReDoc.

## ⚙️ Tech Stack

| Component          | Technology                                     |
|--------------------|------------------------------------------------|
| **Language**       | Python 3.11+                                   |
| **Framework**      | [FastAPI](https://fastapi.tiangolo.com/)       |
| **Database**       | PostgreSQL 13+                                 |
| **ORM**            | SQLAlchemy 2.0 (Synchronous)                   |
| **Migrations**     | Alembic                                        |
| **Authentication** | JWT (PyJWT) & Passlib (for hashing)            |
| **Validation**     | Pydantic v2                                    |
| **Containerization**| Docker & Docker Compose                       |

## 🧰 Project Structure

The backend follows a modular monolith architecture, with each business domain encapsulated in `app/modules/`.

```
orion-backend/
├── app/
│   ├── core/           # Core components (config, database, security)
│   ├── modules/        # Business logic modules (auth, transactions)
│   ├── main.py         # FastAPI application entry point
│   └── dependencies.py   # Shared dependencies (e.g., get_current_user)
├── alembic/            # Database migrations
├── tests/              # Test suite
├── .env.example
├── alembic.ini
├── Dockerfile
└── README.md
```

## 🚀 Quick Start

### 1. Set Up Virtual Environment
From the `orion-backend` directory:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
```
Open the newly created `.env` file and set the following variables:
- `DATABASE_URL`: Your full PostgreSQL connection string.
  - *Example: `DATABASE_URL=postgresql+psycopg2://orion_user:your_password@localhost/orion`*
- `JWT_SECRET_KEY`: A 32-byte hex-encoded secret key. You can generate one with:
  - `openssl rand -hex 32`

### 3. Set Up Database
Ensure your PostgreSQL server is running, then create the database and user:
```sql
CREATE DATABASE orion;
CREATE USER orion_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE orion TO orion_user;
```
Run the database migrations:
```bash
alembic upgrade head
```

### 4. Start the Server
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

## 📝 API Documentation

Once the server is running, explore the interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📋 API Endpoints

All endpoints are prefixed with `/api/v1`.

### Authentication
- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Authenticate and receive a JWT.
- `GET /auth/me`: Get the currently authenticated user's details.

### Transactions
- `POST /transactions`: Create a new transaction.
- `GET /transactions`: List all transactions for the current user.
- `GET /transactions/{id}`: Get a single transaction by ID.
- `PUT /transactions/{id}`: Update a transaction.
- `DELETE /transactions/{id}`: Delete a transaction.

### Analytics (Placeholders)
- `GET /analytics/overview`: Get a financial overview (income, expenses, etc.).
- `GET /analytics/forecast`: Get a forecast of future spending.
- `GET /analytics/trends`: Get data for spending trends over time.

### AI (Placeholders)
- `GET /ai/insights`: Get AI-powered insights on financial habits.

## 🛠 Development

### Code Style
We use `black` for formatting and `isort` for import sorting.
```bash
black .
isort .
```

### Database Migrations
When you change a model in `app/modules/*/models.py`:
```bash
alembic revision --autogenerate -m "Your migration message"
alembic upgrade head
```

## 👥 Contributing
Contributions are welcome! Please fork the repository and open a pull request.

---
Built with ❤️ by the Orion Team