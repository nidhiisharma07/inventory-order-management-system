# Interview Preparation

## Backend

1. Why use a service layer instead of putting logic in FastAPI routes?
2. How does your order creation prevent race conditions on inventory?
3. Explain your global exception handling strategy.
4. When would you use `SELECT FOR UPDATE`?
5. How do Pydantic schemas differ from SQLAlchemy models?

## Frontend

1. How do protected routes work in your React app?
2. Why store JWT in sessionStorage vs localStorage?
3. How does your Axios retry interceptor decide when to retry?
4. What does an Error Boundary catch (and not catch)?
5. How do environment variables work in Vite production builds?

## Docker

1. What is the benefit of multi-stage Docker builds?
2. Why run containers as a non-root user?
3. Difference between `/health` and `/health/ready`?
4. What belongs in `.dockerignore`?
5. How does Docker Compose `depends_on` with healthchecks help?

## Database

1. Explain your Order → OrderItem → Product relationships.
2. Why snapshot `unit_price` on order items?
3. What is Alembic used for?
4. How does a CHECK constraint complement application validation?
5. Trade-offs of soft delete (cancel) vs hard delete for orders?

## JWT Auth

1. What goes inside a JWT payload in your app?
2. Difference between authentication and authorization?
3. Why validate JWT on the server for every protected route?
4. How would you add refresh tokens?
5. Risks of public admin registration?

## Transactions

1. Walk through your order creation transaction step by step.
2. What happens if stock validation fails after partial processing?
3. Why must totals be calculated on the backend?
4. How does cancel order restore inventory atomically?
5. How would you test rollback behavior?
