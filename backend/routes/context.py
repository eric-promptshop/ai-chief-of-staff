from fastapi import APIRouter, UploadFile

router = APIRouter()

@router.post("/context/upload")
def upload_context(file: UploadFile):
    return {"filename": file.filename}