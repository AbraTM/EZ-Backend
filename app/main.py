from fastapi import FastAPI
from app.routers import auth, files

description = """
EZ Backend API

## Authentication

- **Signup and login** with secure JWT tokens (cookie-based).
- Role-based access for **ops** and **client** users.

## Files

- **Upload files** (only for ops users) — supports `.pptx`, `.docx`, `.xlsx`.
- **Generate secure download URLs** (only for client users).
- Download files using encrypted, time-limited URLs.

## Security

- JWT-based access control.
- Encrypted file download tokens.
- Role-based permission checks.
"""

app = FastAPI(
    title="EZ Backend API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Send email to Tushar Malhan",
        "email": "tusharmalhan2564@gmail.com",
    },
)

# Include all the routes
app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {"message": "Secure File Sharing System"}

@app.get("/check-health")
def checkHealth():
    return {"message": "Server is available"}

