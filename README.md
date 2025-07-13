# EZ Backend Intern Assignment

A secure file-sharing system between two different types of users.# EZ Backend Intern Assignment

A secure, role-based backend system built with **FastAPI**, supporting user authentication, file upload, and secure file download with encrypted URLs.

---

## Features

### Authentication

- Signup and login using JWT tokens (stored in HTTP-only cookies).
- Role-based access control: 
  - `ops`: Can upload files.
  - `client`: Can generate secure download links and download files.

---

### File Upload

- Supports file uploads only for **`ops`** users.
- Allowed file types: 
  - `.pptx` (PowerPoint)
  - `.docx` (Word)
  - `.xlsx` (Excel)

---

### Secure File Download

- Generates an encrypted, time-limited download URL for each file.
- Only **`client`** users can access download URLs.
- Protects against unauthorized downloads.

---

## Tech Stack

- **FastAPI** (Python)
- **SQLAlchemy** (PostgreSQL or other SQL DB, currently using Postgres)
- **JWT** (for access tokens)
- **bcrypt** (for secure password hashing)
- **Pydantic** (schema validation)

---


## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ez-backend.git
cd ez-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env file

```bash
SQLALCHEMY_DATABASE_URL = "postgresql://{Postgres_Server_User}:{Postgres_Server_Password}@localhost:5432/EZ_Backend"
JWT_SECRET_KEY = your_jwt_secret
HASH_ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
DOWNLOAD_TOKEN_EXPIRE_MINUTES = 10
DOMAIN = "http://127.0.0.1:8000"

```

### 5. Run database migrations or create tables

```bash
python app.database.create_tables
```

### 6. Start the server
```bash
uvicorn app.main:app --reload
```

## API Docs

Turn on the server first, then visit http://127.0.0.1:8000/docs to access the interactive Swagger UI.
