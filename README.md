# Orion AI Finance 💰

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub stars](https://img.shields.io/github/stars/yourusername/orion-ai-finance?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/orion-ai-finance?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/orion-ai-finance)

> **Orion AI Finance** is a modern financial control hub that leverages AI to help you manage your finances, gain insights, and make data-driven decisions. Built with a modern tech stack for performance, scalability, and clarity.

## ✨ Features

- 📊 **Interactive Dashboards**: Beautiful and responsive visualizations of your financial data.
- 💳 **Full CRUD Transaction Management**: Create, read, update, and delete income and expense records with ease.
- 🔒 **Secure JWT Authentication**: Robust, token-based authentication with secure endpoints for user management.
- 📈 **Financial Analytics**: Access summaries of your financial health, including spending by category.
- 🤖 **AI-Powered Insights**: (In Development) Get smart recommendations and spending forecasts.
- 📱 **Responsive Design**: Works seamlessly on all devices, from mobile to desktop.

## 🛠 Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Components**: Shadcn UI + Radix UI
- **Styling**: Tailwind CSS
- **State Management**: React Query
- **Routing**: React Router

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT & Passlib
- **Validation**: Pydantic
- **Containerization**: Docker

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 13+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/orion-ai-finance.git
cd orion-ai-finance
```

### 2. Set Up the Backend
```bash
cd orion-backend

# Create the environment file from the example
cp .env.example .env
```
Now, open the `.env` file and add your configuration. It requires two main variables:
- `DATABASE_URL`: The connection string for your PostgreSQL database.
  - e.g., `DATABASE_URL=postgresql+psycopg2://user:password@localhost/orion`
- `JWT_SECRET_KEY`: A secret key for signing authentication tokens. Generate one with:
  ```bash
  openssl rand -hex 32
  ```

After configuring your `.env` file, proceed with the setup:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

### 3. Set Up the Frontend
```bash
cd ../  # Back to the project root

# Create the environment file. You may need to create a .env file
# at the root and add your Supabase credentials if you are using them
# for the frontend directly.
npm install
```

### 4. Start the Development Servers
```bash
# In one terminal (from orion-backend/)
uvicorn app.main:app --reload

# In another terminal (from the project root)
npm run dev
```
Navigate to `http://localhost:5173` to see the application.

## 🌐 Project Structure

```
orion-ai-finance/
├── orion-backend/      # FastAPI backend
│   ├── app/
│   │   ├── core/         # Core components (config, db, security)
│   │   ├── modules/      # Business logic (auth, transactions)
│   │   ├── main.py       # FastAPI app entry point
│   │   └── dependencies.py # Shared dependencies (e.g., get_current_user)
│   ├── alembic/        # Database migrations
│   └── tests/
├── src/                # React frontend
│   ├── components/
│   │   ├── layout/       # Layout components (Navbar, Sidebar, etc.)
│   │   └── ui/           # Reusable UI elements (Button, Card, etc.)
│   ├── contexts/       # Global state (Auth, Theme)
│   ├── pages/          # Page components
│   ├── hooks/
│   └── lib/
└── .github/            # GitHub Actions and templates
```

## 📚 Documentation & Writing Style

This project is committed to high-quality, clear, and consistent documentation, following the principles of the **Writing Test Framework**. This includes:
- **Code Comments & Docstrings**: Explaining the "why," not the "how."
- **API Documentation**: Auto-generated from detailed Pydantic schemas and FastAPI route definitions. Access it at `http://localhost:8000/docs` when the backend is running.
- **Commit Messages**: Following the Conventional Commits standard.

## 🧪 Testing

```bash
# Run frontend tests
npm test

# Run backend tests (from orion-backend/)
pytest
```

## 🐳 Docker Setup
For a containerized setup:
```bash
# Build and start services
docker-compose up -d --build

# Run database migrations
docker-compose exec api alembic upgrade head
```

## 🤝 Contributing
Contributions are welcome! Please read our (to-be-created) `CONTRIBUTING.md` guidelines.

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for details.