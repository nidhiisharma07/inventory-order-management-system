# Deployment Guide

## Render (Backend + PostgreSQL)

1. Push repository to GitHub.
2. Create **PostgreSQL** database on Render.
3. Create **Web Service** from `backend/Dockerfile` (or use `render.yaml` Blueprint).
4. Set environment variables:

| Variable | Value |
|----------|--------|
| `ENVIRONMENT` | `production` |
| `DATABASE_URL` | From Render Postgres |
| `JWT_SECRET_KEY` | Long random secret |
| `CORS_ORIGINS` | Your Vercel URL |
| `DEBUG` | `false` |

5. Health check path: `/health/ready`

## Vercel (Frontend)

1. Import GitHub repository.
2. Root directory: `frontend`
3. Build command: `npm run build`
4. Output directory: `dist`
5. Environment variables:

| Variable | Value |
|----------|--------|
| `VITE_API_URL` | `https://your-api.onrender.com` |

6. `vercel.json` handles SPA routing.

## Post-deploy checklist

- [ ] Register first admin user
- [ ] Verify CORS (browser network tab)
- [ ] Test order creation (stock deduction)
- [ ] Confirm `/health/ready` returns 200
