from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.services.input_handler_service import process_input

router = APIRouter()

@router.post("/input")
async def handle_input(
    text: Optional[str] = Form(None),
    user_id: str = Form(...),
    audio: Optional[UploadFile] = File(None),
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None)
):
    result = process_input(text, audio, file, image, user_id)
    return result