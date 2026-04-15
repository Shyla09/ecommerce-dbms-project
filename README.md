# Full-Stack E-Commerce System

This project is a scalable, full-stack e-commerce system using FastAPI (Python Backend), React+Vite+Tailwind (Frontend) and PostgreSQL database.

## System Features
- **User Authentication:** JWT based secure signup/login.
- **Product Listing:** API routing to display registered products.
- **Cart Management:** Endpoints and state mapped logic for active carts.
- **Orders & Tracking:** Cart checkout mechanism handling stock and generating orders + fake payment verification + shipping status mappings.
- **Relational DB:** Complete mapping of Users, Sellers, Products, Orders, Cart, and Payments according to the `schema.sql` guidelines.

---

## 1. Backend Setup (FastAPI)

1. Create a Python Virtual Environment:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Update Datebase Connection:
   In `backend/database.py`, modify `SQLALCHEMY_DATABASE_URL` with your actual Postgres credentials.
   *(Since you have the raw `schema.sql`, you could run `psql -f schema.sql` inside your DB first, or let SQLAlchemy create the schemas automatically on startup via `Base.metadata.create_all(bind=engine)`).*
4. Run the API Server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

---

## 2. Frontend Setup (React setup with Node based tools)

*Note: You need `npm` or `yarn` installed on your machine to start the frontend.*

1. Move to frontend:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

## 3. Database SQL Files

You can examine the pure relational requirements in the newly created `schema.sql`. The logic conforms strongly to constraints, cascades, and types defined there.
