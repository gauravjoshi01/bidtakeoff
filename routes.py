from fastapi import APIRouter, File, UploadFile, HTTPException
from file_processor import process_and_upload_file
import os

router = APIRouter()

# Placeholders for your Azure connection details
AZURE_CONNECTION_STRING = os.environ.get("AZURE_CONNECTION_STRING", "your_connection_string")
AZURE_CONTAINER_NAME = os.environ.get("AZURE_CONTAINER_NAME", "your_container_name")

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # For security reasons, it's better to save the uploaded file to a temporary location
    # and then process it from there, rather than using the raw file path.
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = process_and_upload_file(temp_file_path, AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME)

    # Clean up the temporary file
    os.remove(temp_file_path)

    if "successfully" in result:
        return {"message": result}
    else:
        raise HTTPException(status_code=400, detail=result)
