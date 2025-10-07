# Orion AI Finance 💰

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub stars](https://img.shields.io/github/stars/yourusername/orion-ai-finance?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/orion-ai-finance?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/orion-ai-finance)

> **Orion AI Finance** is a modern financial control hub that leverages AI to help you manage your finances, gain insights, and make data-driven decisions. Built with a modern tech stack for performance and scalability.

## ✨ Features

- 📊 **Interactive Dashboards**: Beautiful visualizations of your financial data
- 🤖 **AI-Powered Insights**: Get smart recommendations and predictions
- 💳 **Transaction Management**: Track income and expenses with ease
- 🔒 **Secure Authentication**: JWT-based authentication with role-based access
- 📱 **Responsive Design**: Works seamlessly on all devices
- 📈 **Financial Analytics**: Comprehensive reporting and trend analysis
- 🚀 **Blazing Fast**: Built with Vite and React for optimal performance

## 🛠 Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Components**: Shadcn UI + Radix UI
- **Styling**: Tailwind CSS
- **State Management**: React Query
- **Form Handling**: React Hook Form

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT
- **Containerization**: Docker

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL 13+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/orion-ai-finance.git
   cd orion-ai-finance
   ```

2. **Set up the backend**
   ```bash
   cd orion-backend
   cp .env.example .env
   # Update .env with your configuration
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   alembic upgrade head
   ```

3. **Set up the frontend**
   ```bash
   cd ../  # Back to project root
   npm install
   cp .env.example .env
   # Update .env with your backend URL
   ```

4. **Start the development servers**
   ```bash
   # In one terminal (backend)
   cd orion-backend
   uvicorn app.main:app --reload

   # In another terminal (frontend)
   npm run dev
   ```

5. **Open your browser** and navigate to `http://localhost:5173`

## 🌐 Project Structure

```
orion-ai-finance/
├── orion-backend/     # FastAPI backend (see backend README)
├── src/               # React frontend
│   ├── components/    # Reusable UI components
│   ├── pages/         # Page components
│   ├── hooks/         # Custom React hooks
│   ├── lib/           # Utility functions
│   └── App.tsx        # Main application component
├── public/            # Static assets
└── .github/           # GitHub workflows and templates
```

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) (requires backend to be running)
- [Frontend Architecture](./docs/frontend-architecture.md)
- [Deployment Guide](./docs/deployment.md)

## 🧪 Testing

```bash
# Run frontend tests
npm test

# Run backend tests
cd orion-backend
pytest
```

## 🐳 Docker Setup

1. **Build and start containers**
   ```bash
   docker-compose up -d --build
   ```

2. **Run database migrations**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [Shadcn UI](https://ui.shadcn.com/) for the beautiful component library
- [Vite](https://vitejs.dev/) for the amazing development experience
- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance backend

---

Built with ❤️ by the Orion Team
