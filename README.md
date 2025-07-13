# EZ Backend Intern Assignment

A secure file-sharing system between two different types of users.

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

---

## Postman Collection

A Postman collection (`EZ Backend(FastAPI).postman_collection.json`) is included to help you test the API easily.

### How to use

1. Import the collection into Postman.
2. Start your FastAPI server locally (`uvicorn app.main:app --reload`).
3. Run the requests in order: **Signup → Login → Upload/List/Generate Download Link → Download**.

**Important:**

- Always start with Signup or Login to set the authentication cookie.
- Check cookies in Postman (top-right near Send) if needed.
- You can modify files or parameters to test different scenarios.

---

## Some of test cases

All API endpoints, request/response schemas, and expected behaviors (including validations) are fully documented in the interactive Swagger UI. You can view and interact with them at http://127.0.0.1:8000/docs#.

I will add detailed written test cases and example steps to this README soon.

---

## How do you plan on deploying this to the production environment?

I would use Docker to containerize the application, which makes it easy to package all dependencies, ensures consistency across environments, and simplifies scaling and updates.

Then, I would set up a reverse proxy server using Nginx, which helps handle incoming traffic efficiently and can help with encryption (HTTPS).

After that, I would deploy it on a cloud VM like Amazon EC2 or Google Cloud Compute Engine, giving me full control over the infrastructure and flexibility to configure resources as needed.

Alternatively, if I just need to deploy it as a standalone API, I can also use managed services like Render, which simplify deployment without having to manage servers manually.
