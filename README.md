# Inventory & Order Management System

Production-ready full-stack platform for managing products, customers, orders, and inventory with JWT authentication, transactional stock control, and cloud deployment support.

[![CI](https://github.com/YOUR_USERNAME/inventory-order-management/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/inventory-order-management/actions/workflows/ci.yml)

## Live Demo (add your URLs)

| Service | URL |
|---------|-----|
| Frontend (Vercel) | `https://your-app.vercel.app` |
| Backend API (Render) | `https://your-api.onrender.com` |
| API Docs (dev only) | `http://localhost:8000/docs` |

## Screenshots

> Add screenshots to `docs/screenshots/` and embed here.

| Dashboard | Orders |
|-----------|--------|
| _placeholder_ | _placeholder_ |

## Features

- Product catalog with SKU uniqueness and low-stock visibility
- Customer management
- Transactional orders with automatic stock deduction and cancel/restore
- JWT auth with admin/staff RBAC
- Paginated order search and sorting
- Dashboard analytics (orders, revenue, recent orders)
- Dockerized local and production deployment
- GitHub Actions CI (lint, test, Docker build)

## Architecture

```text
React (Vite)  --REST/JSON-->  FastAPI API Layer
                                |
                         Service Layer (business rules)
                                |
                         Repository Layer (SQLAlchemy)
                                |
                           PostgreSQL
```

**Backend layers:** `api/` → `services/` → `repositories/` → `models/`  
**Frontend:** `pages/` → `components/` → `api/` (Axios)

## Tech Stack

| Layer | Technologies |
|-------|----------------|
| Backend | FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT, bcrypt |
| Frontend | React 18, Vite, Tailwind CSS, Axios, React Router |
| DevOps | Docker, Docker Compose, GitHub Actions, Render, Vercel |

## Quick Start (Docker)

```bash
cp .env.example .env
# Edit JWT_SECRET_KEY and passwords

docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| Health | http://localhost:8000/health/ready |

Production overlay:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `ENVIRONMENT` | `development` \| `staging` \| `production` |
| `DATABASE_URL` | PostgreSQL connection string |
| `CORS_ORIGINS` | Comma-separated frontend URLs |
| `JWT_SECRET_KEY` | Required strong secret in production |
| `LOG_LEVEL` | `INFO`, `DEBUG`, etc. |

See `backend/.env.production.example` for production template.

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API base URL |
| `VITE_API_TIMEOUT_MS` | Request timeout (default 15000) |
| `VITE_API_MAX_RETRIES` | Retry count for 5xx/network errors |

## API Documentation

### Health

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Liveness |
| `GET /health/ready` | Readiness (includes DB check) |

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register (`role`: admin/staff) |
| POST | `/api/v1/auth/login` | Login → JWT |
| GET | `/api/v1/auth/me` | Current user |

### Products / Customers / Orders / Dashboard

See earlier API sections in codebase or run Swagger at `/docs` in development.

**Admin-only:** create product, delete customer, cancel order.

## Testing

```bash
# Backend
cd backend && pytest -q

# Frontend
cd frontend && npm test

# Lint
cd backend && ruff check app
```

## Deployment

Detailed steps: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

- **Backend:** Render (Docker) + managed PostgreSQL
- **Frontend:** Vercel with `VITE_API_URL` pointing to Render API
- **Blueprint:** `render.yaml` included

## Project Structure

```text
backend/app/
  api/           # HTTP routes
  core/          # Config, logging, middleware, security
  db/            # Session & base
  models/        # SQLAlchemy models
  schemas/       # Pydantic DTOs
  repositories/  # Data access
  services/      # Business logic
  tests/

frontend/src/
  api/           # Axios clients
  components/    # UI components
  context/       # Auth state
  pages/         # Routes
  routes/        # Route guards
```

## Production Hardening

- Structured JSON logging in production
- Global exception handlers (no stack traces leaked)
- CORS restricted to configured origins
- Non-root Docker users + healthchecks
- Multi-stage Docker builds
- JWT secret validation on startup in production
- API docs disabled in production

## Career Resources

- [Resume bullets & ATS content](docs/RESUME.md)
- [Interview questions](docs/INTERVIEW_PREP.md)

## License

MIT (or your chosen license)
