import os
import openai
from blob_service import get_blob_service_client, upload_file_to_blob

# Configure OpenAI API (replace with your actual credentials)
openai.api_type = "azure"
openai.api_base = "YOUR_AZURE_OPENAI_ENDPOINT"  # Placeholder
openai.api_version = "2023-05-15"
openai.api_key = "YOUR_AZURE_OPENAI_KEY"      # Placeholder

def get_file_category(file_name: str) -> str:
    """
    Categorizes the file based on its name using Azure OpenAI.
    """
    try:
        prompt = f"Categorize the following file name into one of these categories: Specification, Plans. File name: {file_name}"
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or your preferred model
            prompt=prompt,
            max_tokens=10
        )
        category = response.choices[0].text.strip()
        if category not in ["Specification", "Plans"]:
            return "Others"
        return category
    except Exception:
        return "Others"

def is_file_type_valid(file_name: str, category: str) -> bool:
    """
    Validates the file type based on its category.
    """
    ext = os.path.splitext(file_name)[1].lower()
    if category == "Specification":
        return ext in [".pdf", ".doc", ".docx"]
    elif category == "Plans":
        return ext == ".pdf"
    return False

def process_and_upload_file(file_path: str, connection_string: str, container_name: str) -> str:
    """
    Processes a file, categorizes it, validates its type, and uploads it to Azure Blob Storage.
    """
    file_name = os.path.basename(file_path)
    category = get_file_category(file_name)

    if category == "Others":
        return f"'{file_name}' is not a specification or a plan."

    if not is_file_type_valid(file_name, category):
        if category == "Specification":
            return f"'{file_name}' is not accepted, accepted format are .pdf or .doc/.docx"
        elif category == "Plans":
            return f"'{file_name}' is not accepted, accepted format are .pdf"

    try:
        with open(file_path, "rb") as data:
            blob_service_client = get_blob_service_client(connection_string)
            if upload_file_to_blob(blob_service_client, container_name, file_name, data):
                return f"'{file_name}' uploaded successfully"
            else:
                return f"Failed to upload '{file_name}'."
    except FileNotFoundError:
        return f"File not found at '{file_path}'."
    except Exception as e:
        return f"An error occurred: {e}"