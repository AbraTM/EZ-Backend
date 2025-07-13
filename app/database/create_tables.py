from app.database.database import Base, engine
from app.models.user import User
from app.models.file import File

print("Creating Tables...")
Base.metadata.create_all(bind=engine)
print("Done!!")