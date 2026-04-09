# Zorvyn Finance Analytics API Documentation

Welcome to the Zorvyn Finance Analytics API documentation! This guide provides a comprehensive overview of the available endpoints, required parameters, and response structures. Additionally, you will find a "Trial Guidance" section to help you get started testing the system immediately.

---

> [!NOTE]  
> **Base URL:** `http://localhost:8000` (or your deployed domain)  
> **Content-Type:** `application/json` (unless specified otherwise)

## Authentication & Authorization
The API uses **OAuth2 with Bearer Tokens (JWT)** for authentication.
Most endpoints require a valid access token in the `Authorization` header:
`Authorization: Bearer <your_access_token>`

### Role-Based Access Control (RBAC)
The system supports three user roles:
- **Admin (`admin`)**: Full access to all endpoints, including user management and system-wide record editing.
- **Analyst (`analyst`)**: Can view financial records and dashboards but cannot alter users or delete data.
- **Viewer (`viewer`)**: Read-only access limited strictly to the dashboard.

---

## Quick Start: Trial Guidance

Follow these steps to seamlessly test the API flows:

1. **Register a User**: 
   - Send a `POST` request to `/users/register` with your `email`, `name`, and `password`.
   - *Note: By default, newly registered users may need admin intervention to receive elevated roles.*
2. **Login and Get Token**: 
   - Send a `POST` request to `/auth/login` using form-data (`username` for email, `password`).
   - Copy the `access_token` returned from the response.
3. **Authorize**: 
   - Attach this token to subsequent requests in the `Authorization: Bearer <token>` header.
4. **Add a Record**: 
   - Send a `POST` request to `/records/` to log an income or expense.
5. **View Analytics**: 
   - Send a `GET` request to `/dashboard/` to retrieve the synthesized analytics.

---

## Modules & Endpoints

### 1. Authentication

#### User Login
**`POST /auth/login`**
Authenticates a user and returns a JWT token.

- **Request Format:** `application/x-www-form-urlencoded`
- **Body Parameters:**
  - `username` (string): The user's registered email.
  - `password` (string): The user's password.
- **Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```
- **Errors:** `401 Unauthorized` (Incorrect credentials), `400 Bad Request` (Inactive user).

---

### 2. User Management
> [!IMPORTANT]  
> Most user management endpoints require **Admin** permissions, except for registration.

#### Register User
**`POST /users/register`**
Creates a new user account.

- **Body (JSON):**
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "securepassword"
  }
  ```

#### List All Users
**`GET /users/`** *(Requires: `admin`)*
Retrieves a list of all registered users.

#### Update User Role
**`PATCH /users/{user_id}/role`** *(Requires: `admin`)*
Updates a user's system role. 
- Acceptable roles: `admin`, `analyst`, `viewer`.

#### Update User Status
**`PATCH /users/{user_id}/status`** *(Requires: `admin`)*
Activates or deactivates a user account.
- **Body:** `{"is_active": true/false}`

---

### 3. Financial Records
These endpoints manage the core financial entries (income and expenses).

#### Create Record
**`POST /records/`** *(Requires: `admin`)*
Logs a new income or expense transaction.

- **Body (JSON):**
  ```json
  {
    "amount": 1500.50,
    "type": "income",
    "category": "freelance",
    "date": "2026-04-06T10:00:00Z",
    "notes": "Project X milestone"
  }
  ```
- **Constraints:**
  - `type`: Must be `"income"` or `"expense"`.
  - `category`: Must be one of `salary, freelance, investment, food, travel, rent, shopping, medical, entertainment, utilities`.

#### List Records
**`GET /records/`** *(Requires: `admin`, `analyst`)*
Retrieves records with optional filtering.

- **Query Parameters:**
  - `type` (optional): Filter by `"income"` or `"expense"`.
  - `category` (optional): Filter by category type.
  - `start_date` / `end_date` (optional): ISO-8601 datetime strings for date range filtering.

#### Update Record
**`PATCH /records/{record_id}`** *(Requires: `admin`)*
Partially updates an existing financial record. Only include fields you wish to change.

#### Delete Record
**`DELETE /records/{record_id}`** *(Requires: `admin`)*
Permanently deletes a financial record.

---

### 4. Dashboard & Analytics

#### View Dashboard Summary
**`GET /dashboard/`** *(Requires: `viewer`, `admin`, `analyst`)*
Retrieves aggregated financial analytics, suitable for visualization.

- **Response (200 OK):**
  ```json
  {
    "total_income": 8500.00,
    "total_expenses": 3200.00,
    "net_balance": 5300.00,
    "category_breakdown": {
      "rent": 1500.00,
      "freelance": 4000.00
    }
  }
  ```
