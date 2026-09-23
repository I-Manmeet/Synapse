from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os
import uuid

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, Header

from orchestrator import run_analysis
from agents.finance_agent import simulate


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
# Auth setup (JWT)
# -----------------------------------

SECRET_KEY = os.getenv("JWT_SECRET", "change-this-secret-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


class AuthRequest(BaseModel):
    email: str
    password: str
    name: str = ""


@app.post("/register")
def register(req: AuthRequest):
    users = _load_users()
    if req.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    users[req.email] = {"password": pwd_context.hash(req.password), "name": req.name}
    _save_users(users)
    return {"success": True, "message": "Account created"}


@app.post("/login")
def login(req: AuthRequest):
    users = _load_users()
    user = users.get(req.email)
    if not user or not pwd_context.verify(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": req.email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "name": user.get("name", "")
    }


def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# -----------------------------------
# Request model
# -----------------------------------

class AnalysisRequest(BaseModel):
    business_id: str
    question: str
    context: str = ""

class SimulationRequest(BaseModel):
    business_id: str
    scenario: str


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
# Upload route  (protected)
# -----------------------------------

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    business_id: str = Form(...),
    user: str = Depends(get_current_user)
):

    try:

        if not business_id.startswith("biz_"):
            raise HTTPException(
                status_code=400,
                detail="Invalid business_id"
            )

        contents = await file.read()

        blob_path = f"{business_id}/{file.filename}"

        print(f"📁 Uploading file to: {blob_path}")

        blob_client = container_client.get_blob_client(blob_path)

        blob_client.upload_blob(
            contents,
            overwrite=True,
            metadata={"business_id": business_id}
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
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------
# Analysis route  (protected)
# -----------------------------------

@app.post("/analyze")
def analyze_business(
    request: AnalysisRequest,
    user: str = Depends(get_current_user)
):

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
            "strategy": result["strategy"],
            "kpis": result["kpis"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------
# Simulate route  (protected)
# -----------------------------------

@app.post("/simulate")
def simulate_scenario(
    request: SimulationRequest,
    user: str = Depends(get_current_user)
):
    try:
        result = simulate(
            scenario=request.scenario,
            business_id=request.business_id
        )
        return {
            "success": True,
            "business_id": request.business_id,
            "scenario": request.scenario,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
