from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os
import uuid

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel

from orchestrator import run_analysis


# -----------------------------------
# Azure Blob Storage
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


# -----------------------------------
# Create FastAPI application
# -----------------------------------

app = FastAPI(
    title="Synapse Multi-Agent Business Assistant",
    description="AI-powered multi-agent business analysis system",
    version="1.0.0"
)


# -----------------------------------
# Generate Business ID
# -----------------------------------

def create_business_id():
    return f"biz_{uuid.uuid4().hex[:8]}"


# -----------------------------------
# Create New Business Workspace
# -----------------------------------

@app.post("/create-business")
async def create_business():

    business_id = create_business_id()

    return {
        "success": True,
        "business_id": business_id,
        "message": "Business workspace created successfully"
    }


# -----------------------------------
# Request model
# -----------------------------------

class AnalysisRequest(BaseModel):
    business_id: str
    question: str
    context: str = ""


# -----------------------------------
# Home route
# -----------------------------------

FRONT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "frontend"
)


@app.get("/")
def home():
    return FileResponse(
        os.path.join(FRONT, "index.html")
    )


@app.get("/{page}.html")
def page(page: str):
    return FileResponse(
        os.path.join(FRONT, f"{page}.html")
    )


# -----------------------------------
# Upload route
# -----------------------------------

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    business_id: str = Form(...)
):

    try:

        # -----------------------------------
        # Validate Business ID
        # -----------------------------------

        if not business_id.startswith("biz_"):
            raise HTTPException(
                status_code=400,
                detail="Invalid business_id"
            )

        # -----------------------------------
        # Read uploaded file
        # -----------------------------------

        contents = await file.read()

        # -----------------------------------
        # Create business-specific blob path
        # -----------------------------------

        blob_path = f"{business_id}/{file.filename}"

        print(
            f"📁 Uploading file to: {blob_path}"
        )

        # -----------------------------------
        # Upload to Azure Blob Storage
        # -----------------------------------

        blob_client = container_client.get_blob_client(
            blob_path
        )

        blob_client.upload_blob(
            contents,
            overwrite=True,
             metadata={
        "business_id": business_id
    }
        )

        return {
            "success": True,
            "business_id": business_id,
            "filename": file.filename,
            "blob_path": blob_path,
            "content_type": file.content_type,
            "size_bytes": len(contents),
            "storage": "Azure Blob Storage",
            "container": "synapse-documents",
            "message": "File uploaded successfully to Azure Blob Storage"
        }

    except HTTPException:
        raise

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
            context=request.context,
            business_id=request.business_id
        )

        return {
            "success": True,
            "business_id": request.business_id,
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