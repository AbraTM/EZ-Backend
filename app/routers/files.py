from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.auth import get_current_user
from app.utils.file_token import generate_download_token, verify_download_token
from app.models.user import User
from app.models.file import File as FileModel
from app.schemas.file import FileOut
from dotenv import load_dotenv
import uuid
import os

load_dotenv()
DOMAIN = os.getenv("DOMAIN")

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


@router.get("/list")
def list_files(db: Session = Depends(get_db)):
    files_list = db.query(FileModel).all()
    return files_list

@router.get("/generate-download-link/{file_id}")
def generate_download_link(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type.value != "client":
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Client Users are allowed to generate download URLs.")
    
    db_file = db.query(FileModel).filter(file_id == file_id).first()
    if not db_file:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
    
    token = generate_download_token(file_id)
    download_url = f"{DOMAIN}/files/download/{token}"
    return {"download_url": download_url}

@router.get("/download/{token}")
def download_file(
    token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type.value != "client":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Client Users are allowed to generate download URLs.")
    
    file_id = verify_download_token(token)
    if not file_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token.")
    
    db_file = db.query(FileModel).filter(file_id == file_id).first()

    return FileResponse(path=db_file.file_path, filename=db_file.file_name)