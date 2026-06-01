# Resume Content

## Project Title

**Inventory & Order Management System**

## One-Line Description

Full-stack inventory and order platform with JWT auth, transactional stock control, and Dockerized deployment on Render + Vercel.

## ATS-Friendly Bullet Points

- Built a production-ready Inventory & Order Management System using FastAPI, React, PostgreSQL, and Docker with clean layered architecture (routers, services, repositories).
- Implemented transactional order processing with row-level locking, automatic inventory deduction, and rollback on failure to prevent overselling.
- Designed REST APIs with pagination, search, sorting, Pydantic validation, and role-based access control (admin/staff) using JWT authentication.
- Developed responsive React UI with protected routes, debounced search, real-time order totals, and dashboard analytics.
- Containerized services with multi-stage Dockerfiles, health checks, non-root users, and GitHub Actions CI for lint, test, and image builds.
- Deployed backend to Render and frontend to Vercel with environment-based configuration and CORS hardening.

## Tech Stack Summary

**Backend:** Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT, bcrypt, Pydantic  
**Frontend:** React, Vite, Tailwind CSS, Axios, React Router  
**DevOps:** Docker, Docker Compose, GitHub Actions, Render, Vercel  
**Practices:** REST, RBAC, transactional DB design, structured logging, CI/CD
