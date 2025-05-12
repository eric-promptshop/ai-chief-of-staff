# AI Chief of Staff 🤖

[![Backend CI](https://github.com/yourusername/ai-chief-of-staff/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/yourusername/ai-chief-of-staff/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/yourusername/ai-chief-of-staff/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/yourusername/ai-chief-of-staff/actions/workflows/frontend-ci.yml)
[![Deploy](https://github.com/yourusername/ai-chief-of-staff/actions/workflows/deploy.yml/badge.svg)](https://github.com/yourusername/ai-chief-of-staff/actions/workflows/deploy.yml)

An intelligent AI-first orchestration layer that manages a digital workforce of agents. This Chief of Staff enables users to delegate tasks, configure agent autonomy, and oversee execution using explainable, secure, and context-aware AI interactions.

## 🌟 Features

- Natural language task delegation
- Dynamic agent configuration using Microsoft AutoGen
- Task completion and decision logging with Supabase
- Multi-agent chat threads with explainability
- Modern UI with Vercel deployment
- Document upload and RAG-based context awareness
- Adjustable agent autonomy levels

## 🛠️ Tech Stack

- **Frontend:** React + Tailwind CSS (Vercel deployment)
- **Backend:** FastAPI (Python)
- **Database:** Supabase (PostgreSQL)
- **Vector Storage:** Pinecone
- **Agent Framework:** Microsoft AutoGen
- **Authentication:** Supabase Auth

## 🚀 Getting Started

### Prerequisites

- Node.js (v16+)
- Python (3.9+)
- Git

### Environment Variables

Copy `.env.example` to `.env` in both frontend and backend directories and fill in the required values:

#### Backend Environment Variables

```
# Application settings
DEBUG=False                          # Enable/disable debug mode

# Supabase settings
SUPABASE_URL=your_supabase_url       # URL of your Supabase project
SUPABASE_KEY=your_supabase_key       # API key for Supabase access
SUPABASE_JWT_SECRET=your_jwt_secret  # JWT secret for auth verification

# Pinecone settings
PINECONE_API_KEY=your_pinecone_api_key         # API key for Pinecone access
PINECONE_ENVIRONMENT=your_pinecone_environment # Pinecone environment (e.g., 'us-west1-gcp')
PINECONE_INDEX_NAME=your_pinecone_index_name   # Name of your Pinecone vector index

# OpenAI settings
OPENAI_API_KEY=your_openai_api_key   # API key for OpenAI used with AutoGen

# Database URL
DATABASE_URL=your_database_url       # Full connection URL for the database
```

#### Frontend Environment Variables

```
# API Settings
VITE_API_URL=http://localhost:8001/api/v1  # Backend API URL

# Supabase settings
VITE_SUPABASE_URL=your_supabase_url        # URL of your Supabase project
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key  # Anonymous API key for Supabase

# Application settings
VITE_APP_NAME=AI Chief of Staff            # Application name
VITE_APP_VERSION=1.0.0                     # Application version

# Feature flags
VITE_ENABLE_ANALYTICS=false                # Toggle analytics features
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-chief-of-staff.git
   cd ai-chief-of-staff
   ```

2. Set up frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Set up backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

## 📁 Project Structure

```
.
├── frontend/               # React + Tailwind frontend
│   ├── src/               # Source code
│   ├── public/            # Static files
│   └── package.json       # Frontend dependencies
├── backend/               # FastAPI backend
│   ├── main.py           # Application entry point
│   ├── routes/           # API routes
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   └── requirements.txt  # Backend dependencies
├── agents/               # AutoGen agent definitions
├── docs/                 # Documentation
├── .github/              # GitHub workflows and templates
└── CONTRIBUTING.md       # Contribution guidelines
```

## 🧪 Testing

- Frontend: `cd frontend && npm test`
- Backend: `cd backend && pytest`

## 📚 Documentation

- [Development Guide](docs/development.md)
- [API Documentation](http://localhost:8001/docs) (when backend is running)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🤝 Contributing

Contributions are welcome! Please check out our [contributing guidelines](CONTRIBUTING.md) for details on how to get started. We use GitHub issues for tracking requests and bugs.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Microsoft AutoGen](https://github.com/microsoft/autogen)
- [Supabase](https://supabase.io)
- [Pinecone](https://www.pinecone.io)
- [FastAPI](https://fastapi.tiangolo.com)
- [React](https://reactjs.org)
- [Tailwind CSS](https://tailwindcss.com)

# Backend Setup (FastAPI)

## Prerequisites
- Python 3.11 (installed via Homebrew: `brew install python@3.11`)
- Virtual environment created: `python3.11 -m venv venv311`

## Setup Steps
1. Activate the environment:
   ```sh
   source venv311/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```
4. Test the health check endpoint:
   - Visit [http://localhost:8000/health](http://localhost:8000/health)
   - You should see: `{ "status": "healthy", "service": "autogen-playground-api" }` 