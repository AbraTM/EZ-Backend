from fastapi import FastAPI
from app.routers import auth, files

app = FastAPI()

# Include all the routes
app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {"message": "Secure File Sharing System"}

@app.get("/check-health")
def checkHealth():
    return {"message": "Server is available"}

