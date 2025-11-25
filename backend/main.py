import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from database import init_db, get_db, Transaction, Goal
from parser import parse_csv
from pydantic import BaseModel

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

# API Routes (defined BEFORE static files)
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV.")
    
    contents = await file.read()
    
    # Upload to GCS if configured
    bucket_name = os.getenv("GCS_BUCKET")
    if bucket_name and bucket_name != "walletgenie-bucket":
        try:
            from google.cloud import storage
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(f"uploads/{file.filename}")
            blob.upload_from_string(contents, content_type=file.content_type)
            print(f"Uploaded {file.filename} to GCS bucket {bucket_name}")
        except Exception as e:
            print(f"Failed to upload to GCS: {e}")

    transactions_data = parse_csv(contents)
    
    if not transactions_data:
        raise HTTPException(status_code=400, detail="Could not parse CSV or empty file.")
    
    # Insert into DB
    count = 0
    for data in transactions_data:
        txn = Transaction(**data)
        db.add(txn)
        count += 1
    
    db.commit()
    
    return {"message": "File uploaded successfully", "rows_inserted": count}

@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    from services import get_summary_data
    return get_summary_data(db)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.post("/chat")
def chat(request: ChatRequest):
    from agent import chat_with_agent
    response = chat_with_agent(request.message, request.session_id)
    return {"response": response}

# Mount static files at root (AFTER API routes)
# This will serve the Angular app and handle client-side routing
if os.path.exists("/app/static"):
    app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
