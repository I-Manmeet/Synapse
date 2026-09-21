from azure.identity import DefaultAzureCredential  # type: ignore[reportMissingImports]
from azure.ai.projects import AIProjectClient  # type: ignore[reportMissingImports]

from config import FOUNDRY_PROJECT_ENDPOINT


credential = DefaultAzureCredential()

project_client = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=credential
)

print("Connected to Azure Foundry!")