import logging  
from azure.storage.blob import BlobServiceClient  
from azure.core.exceptions import ResourceExistsError  
  
logger = logging.getLogger(__name__)  
  
def get_blob_service_client(connection_string: str) -> BlobServiceClient:  
    """Create and return a BlobServiceClient."""  
    return BlobServiceClient.from_connection_string(connection_string)  
  
def upload_file_to_blob(blob_service_client, container_name, file_name, file_content) -> bool:  
    """Uploads a file's content to a specified Azure Blob Storage container."""  
    try:  
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)  
  
        # Create the container if it doesn't exist  
        try:  
            container_client = blob_service_client.get_container_client(container_name)  
            container_client.create_container()  
            logger.info(f"Container '{container_name}' created.")  
        except ResourceExistsError:  
            logger.info(f"Container '{container_name}' already exists.")  
  
        logger.info(f"Uploading '{file_name}' to container '{container_name}'...")  
        blob_client.upload_blob(file_content, overwrite=True)  
        logger.info(f"Successfully uploaded '{file_name}'.")  
        return True  
    except Exception as e:  
        logger.error(f"Failed to upload '{file_name}' to blob storage: {e}")  
        return False  
