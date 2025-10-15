import os  
import logging  
from fastapi import APIRouter, File, UploadFile, HTTPException  
from dotenv import load_dotenv  
from blob_service import get_blob_service_client, upload_file_to_blob  
  
# Load environment variables  
load_dotenv()  
  
# Configure logging  
logging.basicConfig(  
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"  
)  
logger = logging.getLogger(__name__)  
  
# Azure Blob Storage settings  
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")  
AZURE_BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME", "local-uploads")  
  
router = APIRouter()  
  
@router.post("/upload")  
async def upload_file(file: UploadFile = File(...)):  
    """API endpoint to upload a file to Azure Blob Storage."""  
    if not AZURE_STORAGE_CONNECTION_STRING:  
        raise HTTPException(status_code=500, detail="Azure Storage connection string not configured.")  
  
    try:  
        blob_service_client = get_blob_service_client(AZURE_STORAGE_CONNECTION_STRING)  
        file_content = await file.read()  
  
        success = upload_file_to_blob(  
            blob_service_client=blob_service_client,  
            container_name=AZURE_BLOB_CONTAINER_NAME,  
            file_name=file.filename,  
            file_content=file_content  
        )  
  
        if success:  
            return {"status": "success", "filename": file.filename}  
        else:  
            raise HTTPException(status_code=500, detail="Failed to upload file to Azure Blob Storage.")  
  
    except Exception as e:  
        logger.critical(f"Error in upload_file API: {e}")  
        raise HTTPException(status_code=500, detail=str(e))  
