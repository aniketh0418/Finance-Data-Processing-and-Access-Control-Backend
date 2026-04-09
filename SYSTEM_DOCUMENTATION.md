# Zorvyn Backend System Architecture

This document provides a holistic view of the internal construction, module breakdown, and architectural decisions made for the Zorvyn Finance Analytics Backend. 

---

## 1. System Overview
Zorvyn is a modular, high-performance financial data processing API. It is designed around the principles of **FastAPI** leveraging asynchronous I/O with **MongoDB** to deliver fast, secure, and scalable endpoints for tracking incomes, expenses, and synthesizing financial dashboards via role-based access control (RBAC).

## 2. Technology Stack
- **Framework:** FastAPI (Python 3.x)
- **Database:** MongoDB
- **DB Async Driver:** Motor (Asyncio driver for MongoDB)
- **Validation:** Pydantic V2
- **Authentication:** OAuth2 with JWT (JSON Web Tokens)
- **Cryptograpghy:** Passlib (bcrypt)
- **Server:** Uvicorn

---

## 3. Core Architecture
The system operates on an **N-Tier Architecture** style, heavily promoting separation of concerns. The codebase is broken down into specific layers:

1. **Routing Layer (`routes/`)**: Handles HTTP requests, input parameter validation, and delegates business logic to the service layer.
2. **Service/Business Logic Layer (`services/`)**: Contains the core business logic (CRUD operations, aggregations). Abstracted away from HTTP contexts.
3. **Data Access Layer (`config.database`)**: Centralized MongoDB connection management.
4. **Schema Layer (`schemas/`)**: Pydantic models handling request/response serialization, typing, and data validation bounds.
5. **Security Layer (`core/`)**: Middleware and dependency injectors managing JWT encoding, decoding, password hashing, and endpoint role protection.

---

## 4. Module Listing & Features

### A. Authentication & Security Module
Responsible for validating user identities and issuing secure session tokens.
- **Features:** 
  - Password hashing utilizing the `bcrypt` algorithm.
  - Generates secure, short-lived JWT tokens on successful logins.
  - Provides FastAPI dependency injection for current user extraction.

### B. User Management Module
Handles the provisioning and status tracking of system users.
- **Features:**
  - Secure user registration flow.
  - System-wide **Role-Based Access Control (RBAC)** tracking:
    - `admin`: Superuser privileges.
    - `analyst`: Financial viewer and auditor.
    - `viewer`: Dashboard-only access.
  - Account status toggles (activate/deactivate).

### C. Financial Data Processing Module
The primary engine for logging and managing financial transactions.
- **Features:**
  - Robust Pydantic bounds checking. Rejects negative transaction amounts and enforces strict categorizations (e.g., `salary`, `freelance`, `rent`, `utilities`).
  - Distinguishes clearly between `income` and `expense` types.
  - Exposes flexible querying capabilities enabling records to be filtered by arbitrary date ranges, categories, and types.

### D. Analytics & Dashboard Module
Synthesizes raw transactional data into actionable insights.
- **Features:**
  - Performs complex MongoDB Aggregation Pipelines to calculate net balances.
  - Automatically calculates real-time breakdown dictionaries of expenses and incomes structured by category.

---

## 5. Directory Structure
```text
zorvyn/
├── config/
│   └── database.py        # MongoDB initialization, connection pooling, and configuration
├── core/
│   ├── auth.py            # OAuth2 dependencies and RBAC middleware
│   └── security.py        # Password hashing and JWT token builders
├── models/                # Reserved for more persistent ORM/ODM models if needed
├── routes/
│   ├── auth_routes.py     # Authentication endpoints
│   ├── dashboard_routes.py# Analytics endpoints
│   ├── record_routes.py   # Financial ledger endpoints
│   └── user_routes.py     # User tracking and registration endpoints
├── schemas/
│   ├── record.py          # Data validation schemas for records
│   ├── token.py           # Data validation schemas for JWT
│   └── user.py            # Data validation schemas for user entries
├── services/
│   ├── dashboard_service.py # Aggregation logic
│   ├── record_service.py    # Record CRUD logic
│   └── user_service.py      # User management logic
├── main.py                # FastApi application instance and lifespans
├── requirements.txt       # Project dependencies
└── .env                   # Environment variables (DB URI, Secrets)
```

---

## 6. Database Schema Design (MongoDB Document Strategy)

### Collection: `users`
- **Fields**: `_id` (ObjectId), `name` (String), `email` (String, Indexed), `password_hash` (String), `role` (String), `is_active` (Boolean), `created_at` (Datetime).

### Collection: `records`
- **Fields**: `_id` (ObjectId), `amount` (Float), `type` (String: income/expense), `category` (String), `date` (Datetime), `notes` (String), `created_by` (String representation of User ID), `created_at` (Datetime).

---

## 7. Next Steps for Scalability
Given the foundational structure, features can be safely expanded without cluttering existing code:
1. **Caching Layer:** Redis can be easily hooked into `dashboard_service.py` for aggregation caching.
2. **Testing:** The separation of the `services/` layer enables mock testing of the database independently of FastAPI HTTP tests in `routes/`.
