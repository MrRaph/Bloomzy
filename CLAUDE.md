# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bloomzy is a collaborative platform for intelligent management of indoor plants and gardens, integrating community features, notifications, and AI. The project follows a microservices architecture with Flask backend and Vue.js frontend.

## Development Commands

### Backend (Flask/Python)
```bash
cd backend
make venv          # Create virtual environment and install dependencies
make test          # Run all pytest tests
make clean         # Clean virtual environment and Python cache files
```

### Manual backend setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev
```

## Architecture

### Backend Structure
- **Flask Application Factory**: `backend/app/__init__.py` uses `create_app()` pattern
- **SQLAlchemy Models**: Located in `backend/models/` (e.g., `user.py`)
- **Blueprint Routes**: Organized in `backend/routes/` (e.g., `auth.py`)
- **JWT Authentication**: Implemented with PyJWT, includes blacklist for logout
- **Database**: Uses SQLite in-memory for development, PostgreSQL planned for production

### Authentication System
- JWT-based authentication with refresh tokens
- Password hashing using `pbkdf2:sha256` method
- JWT blacklist stored in memory (production should use Redis)
- Protected routes use `@jwt_required` decorator

### API Endpoints
- Authentication routes under `/auth` prefix:
  - `POST /auth/signup` - User registration with email validation
  - `POST /auth/login` - User authentication
  - `POST /auth/refresh` - Token refresh
  - `POST /auth/logout` - Token invalidation
  - `GET /auth/protected` - Protected endpoint example

### Testing
- Uses pytest with fixtures in `backend/tests/conftest.py`
- Test organization by feature: `backend/tests/auth/`
- TDD methodology is mandatory (tests before code)

## Development Guidelines

### Project Methodology
- **TDD Required**: Write tests before implementing features - mandatory for all functionality
- **Git Flow**: Feature branches, PRs, merge to main after validation
- **Documentation**: Keep all docs in `docs/` directory up to date
- **Code Quality**: Factorization and non-repetition - share code and tests whenever possible

### Definition of Done
A feature is considered complete only when:
- It is tested (unit + integration tests)
- It is functional
- It is documented
- It has undergone PR review and validation

### Backend Best Practices
- Use environment variables for sensitive configuration (SECRET_KEY)
- Follow Flask blueprint pattern for route organization
- Implement proper error handling with HTTP status codes
- Use SQLAlchemy for database operations
- Password validation: minimum 8 characters, mixed alphanumeric
- See `docs/backend/best_practices.md` for detailed guidelines

## Directory Structure

```
backend/
├── app/              # Flask application factory
├── models/           # SQLAlchemy models
├── routes/           # Blueprint routes
├── tests/            # Test files organized by feature
├── Makefile          # Build automation
└── requirements.txt  # Python dependencies

frontend/
├── src/              # Vue.js source code
└── tests/            # Frontend tests

docs/
├── backend/          # Backend documentation
├── prds/             # Product Requirements Documents (always consult before modifications)
├── todos/            # Task tracking and development steps
└── gh.md             # GitHub workflow and project management
```

## Key Technologies

### Backend Stack
- Flask 3.0.0 with SQLAlchemy
- JWT authentication (PyJWT 2.8.0)
- Pytest for testing
- Werkzeug for password hashing

### Target Architecture (from PRD)
- Microservices with Docker containerization
- PostgreSQL + Redis for production
- Elasticsearch for search functionality
- Monitoring with Prometheus/Grafana

## Testing Strategy

Run tests with: `cd backend && make test`

Test files are organized by feature in `backend/tests/`:
- `auth/` - Authentication tests
- `conftest.py` - Shared test fixtures

## Reference Documentation

### PRDs (Product Requirements Documents)
Always consult these before making modifications:
- `docs/prds/bloomzy_prd_general.md` - General specifications
- `docs/prds/bloomzy_prd_architecture.md` - Technical architecture
- `docs/prds/bloomzy_prd_auth.md` - Authentication system
- `docs/prds/bloomzy_prd_community.md` - Community features
- `docs/prds/bloomzy_prd_garden.md` - Garden management
- `docs/prds/bloomzy_prd_indoor_plants.md` - Indoor plant features
- `docs/prds/bloomzy_prd_notifications.md` - Notification system
- `docs/prds/bloomzy_prd_ai_integration.md` - AI integration

### TODO Lists
Development steps are organized in:
- `docs/todos/todo_auth.md` - Authentication tasks
- `docs/todos/todo_indoor_plants.md` - Indoor plant tasks
- `docs/todos/todo_garden.md` - Garden tasks
- `docs/todos/todo_notifications.md` - Notification tasks
- `docs/todos/todo_ai_integration.md` - AI integration tasks
- `docs/todos/todo_community.md` - Community tasks
- `docs/todos/todo_architecture.md` - Architecture tasks

### GitHub Workflow
- See `docs/gh.md` for complete workflow: issues, projects, PRs, labels
- Use `gh` CLI commands for project management
- GitHub Project: "Bloomzy Roadmap" (ID 3)
- Labels: auth, indoor, garden, notifications, ai, community, architecture

## Important Notes

- **Always start by consulting PRDs and TODO files before any modification**
- Virtual environment must be created in `backend/.venv/`
- Secret keys should never be hardcoded (use environment variables)
- Current JWT blacklist is in-memory; production needs persistent storage
- Database is SQLite in-memory for development
- All API endpoints should return appropriate HTTP status codes
- Email validation uses regex pattern
- reCAPTCHA token validation is implemented for signup