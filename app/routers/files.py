from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.auth import get_current_user
from app.models.user import User
from app.models.file import File as FileModel
from app.schemas.file import FileOut
import uuid
import shutil
import os

ALLOWED_TYPES = [
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # pptx
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",    # docx
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",          # xlsx
]

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
def uploadFile(
    uploaded_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    if current_user.user_type.value != "ops":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Operations Users are allowed to upload files.")
    
    if uploaded_file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a file of type pptx, docx or xlsx only.")
    
    # Creating a unique file name
    file_ext = uploaded_file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Read file content
    file_content = uploaded_file.file.read()
    file_size = len(file_content)
    # Write to disk
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    db_file = FileModel(
        file_name=uploaded_file.filename,
        file_type=file_ext,
        file_size=file_size,
        file_path=file_path,
        uploaded_by=current_user.id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    file_out = FileOut.model_validate(db_file)

    return {"message" : "File successfully uploaded", "file": file_out}

