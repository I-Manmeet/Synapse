from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel

from orchestrator import run_analysis


# -----------------------------------
# Create FastAPI application
# -----------------------------------
storage_account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL")

credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url=storage_account_url,
    credential=credential
)

container_client = blob_service_client.get_container_client(
    "synapse-documents"
)
app = FastAPI(
    title="Synapse Multi-Agent Business Assistant",
    description="AI-powered multi-agent business analysis system",
    version="1.0.0"
)


# -----------------------------------
# Request model
# -----------------------------------

class AnalysisRequest(BaseModel):
    question: str
    context: str = ""


# -----------------------------------
# Home route
# -----------------------------------





FRONT = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
def home():
    return FileResponse(os.path.join(FRONT, "index.html"))

@app.get("/{page}.html")
def page(page: str):
    return FileResponse(os.path.join(FRONT, f"{page}.html"))


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        blob_client = container_client.get_blob_client(file.filename)

        blob_client.upload_blob(
            contents,
            overwrite=True
        )

        return {
            "success": True,
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
            "storage": "Azure Blob Storage",
            "container": "synapse-documents",
            "message": "File uploaded successfully to Azure Blob Storage"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -----------------------------------
# Analysis route
# -----------------------------------

@app.post("/analyze")
def analyze_business(request: AnalysisRequest):

    try:

        result = run_analysis(
            question=request.question,
            context=request.context
        )

        return {
            "success": True,
            "question": request.question,
            "report": result["final_report"],
            "analytics": result["findings"].get("analytics"),
            "finance": result["findings"].get("finance"),
            "market": result["findings"].get("market"),
            "customer": result["findings"].get("customer"),
            "risk": result["risk"],
            "strategy": result["strategy"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )