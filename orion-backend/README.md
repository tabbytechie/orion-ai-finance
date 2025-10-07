# Orion Backend API 💻

> "Built with clarity, powered by intelligence." 🌌

![GitHub](https://img.shields.io/github/license/yourusername/orion-ai-finance)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-4169E1?logo=postgresql&logoColor=white)

This repository contains the backend for the **Orion AI-Powered Financial Control Hub** - a high-performance, modular API built with Python, FastAPI, and PostgreSQL. The backend provides secure, scalable endpoints for financial data processing, user authentication, and AI-powered insights.

## 💡 Key Features

- 💰 **Financial Data Management**: Secure CRUD operations for transactions, accounts, and categories
- 🔑 **JWT Authentication**: Secure user authentication with role-based access control
- 📊 **Data Analytics**: Built-in financial analytics and reporting endpoints
- 🤖 **AI Integration**: AI-powered insights and recommendations
- 📦 **Modular Architecture**: Clean separation of concerns for maintainability
- 🛠 **Production Ready**: Containerized with Docker, ready for deployment
- 📝 **Comprehensive Documentation**: Interactive API docs with OpenAPI (Swagger UI)

## ⚙️ Tech Stack

| Component             | Technology                                                                 |
|-----------------------|----------------------------------------------------------------------------|
| **Language**          | Python 3.11+                                                              |
| **Framework**         | [FastAPI](https://fastapi.tiangolo.com/)                                   |
| **Database**          | PostgreSQL 13+                                                            |
| **ORM**               | SQLAlchemy 2.0+ with async support                                        |
| **Migrations**        | Alembic                                                                   |
| **Authentication**    | JWT (PyJWT) with password hashing                                         |
| **Validation**        | Pydantic v2                                                               |
| **Containerization**  | Docker & Docker Compose                                                   |

## 🧰 Project Structure

The backend follows a **Modular Monolith** architecture, where each business domain is encapsulated in its own module under `app/modules/`. This approach provides a good balance between maintainability and development speed.

```
orion-backend/
├── app/
│   ├── core/                 # Core application components
│   │   ├── __init__.py
│   │   ├── config.py           # Application configuration
│   │   ├── database.py         # Database connection and session management
│   │   └── security.py         # Authentication and security utilities
│   ├── modules/              # Business logic modules
│   │   ├── auth/               # Authentication module
│   │   ├── transactions/       # Transaction management
│   │   └── ai/                 # AI and analytics features
│   ├── main.py               # FastAPI application factory
│   └── dependencies.py       # Shared FastAPI dependencies
├── alembic/              # Database migrations
│   ├── versions/            # Migration scripts
│   ├── env.py               # Migration environment
│   └── script.py.mako       # Migration template
├── tests/                # Test suite
├── .env.example          # Environment variables template
├── .gitignore
├── alembic.ini           # Alembic configuration
├── docker-compose.yml    # Local development setup
├── Dockerfile            # Production Dockerfile
├── pyproject.toml        # Project metadata and dependencies
└── README.md             # This file
```

### Module Structure

Each module in `app/modules/` follows this structure:

```
module_name/
├── __init__.py           # Module exports
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic models for request/response
├── routes.py            # API endpoints
├── service.py           # Business logic
└── tests/               # Module-specific tests
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 13+
- Git
- (Optional) Docker & Docker Compose

### Option 1: Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/orion-ai-finance.git
   cd orion-ai-finance/orion-backend
   ```

2. **Set up a virtual environment**
   ```bash
   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # For Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   - Make sure PostgreSQL is running
   - Create a new database:
     ```sql
     CREATE DATABASE orion;
     CREATE USER orion_user WITH PASSWORD 'your_secure_password';
     GRANT ALL PRIVILEGES ON DATABASE orion TO orion_user;
     ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your database credentials and generate a secure JWT secret:
   ```bash
   echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" >> .env
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

### Option 2: Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/orion-ai-finance.git
   cd orion-ai-finance/orion-backend
   ```

2. **Copy and configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

3. **Build and start services**
   ```bash
   docker-compose up -d --build
   ```

4. **Run migrations**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

The API will be available at `http://localhost:8000`

### 📝 API Documentation

Once the server is running, explore the API documentation:

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Authenticate and get JWT token
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user details

### Transactions
- `GET /api/v1/transactions` - List all transactions
- `POST /api/v1/transactions` - Create a new transaction
- `GET /api/v1/transactions/{id}` - Get transaction details
- `PUT /api/v1/transactions/{id}` - Update a transaction
- `DELETE /api/v1/transactions/{id}` - Delete a transaction

### Analytics
- `GET /api/v1/analytics/overview` - Financial overview
- `GET /api/v1/analytics/categories` - Spending by category
- `GET /api/v1/analytics/trends` - Spending trends over time

### AI Features
- `GET /api/v1/ai/insights` - AI-powered financial insights
- `POST /api/v1/ai/analyze` - Analyze financial data

## 🛠 Development

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app --cov-report=term-missing
```

### Code Style
We use `black` for code formatting and `isort` for import sorting:
```bash
# Format code
black .

# Sort imports
isort .
```

### Database Migrations
When making changes to models, create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👀 Show Your Support

Give a ⭐ if this project helped you!

---

Built with ❤️ by the Orion Team