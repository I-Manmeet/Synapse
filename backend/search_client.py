from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
import os

load_dotenv()


# ==========================================
# Azure AI Search Configuration
# ==========================================

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


# ==========================================
# Search Business Documents
# ==========================================

def search_documents(
    query: str,
    business_id: str,
    top: int = 5
):
    """
    Search Azure AI Search ONLY within the specified
    business workspace.
    """

    if not business_id:
        raise ValueError(
            "business_id is required for business-isolated search."
        )

    # -----------------------------------
    # Filter results by business_id
    # -----------------------------------

    filter_expression = (
        f"business_id eq '{business_id}'"
    )

    results = search_client.search(
        search_text=query,
        filter=filter_expression,
        top=top
    )

    documents = []

    for result in results:

        documents.append({
            "id": result.get("id"),
            "content": result.get("content"),
            "file_name": result.get(
                "metadata_storage_name"
            ),
            "content_type": result.get(
                "metadata_storage_content_type"
            ),
            "business_id": result.get(
                "business_id"
            )
        })

    return documents