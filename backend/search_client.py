from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
import os

load_dotenv()

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
INDEX_NAME = "synapse-business-index"

if not SEARCH_ENDPOINT:
    raise ValueError(
        "AZURE_SEARCH_ENDPOINT is missing from .env"
    )

credential = DefaultAzureCredential()

search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=credential
)


def search_documents(query: str, top: int = 5):

    results = search_client.search(
        search_text=query,
        top=top
    )

    documents = []

    for result in results:
        documents.append({
            "id": result.get("id"),
            "content": result.get("content"),
            "file_name": result.get("metadata_storage_name"),
            "content_type": result.get(
                "metadata_storage_content_type"
            )
        })

    return documents