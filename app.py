from fastapi import FastAPI  
from routes import router as blob_router  
  
app = FastAPI()  
  
# Include routes  
app.include_router(blob_router)  
  
@app.get("/")  
def root():  
    return {"message": "Azure Blob Upload API is running"}  
