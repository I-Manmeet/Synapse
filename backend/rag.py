from search_client import search_documents


def retrieve_context(
    question: str,
    business_id: str,
    top: int = 5
) -> str:
    """
    Retrieve relevant business information from Azure AI Search
    for ONLY the specified business workspace.
    """

    if not business_id:
        raise ValueError(
            "business_id is required for business-isolated search."
        )

    documents = search_documents(
        query=question,
        top=top,
        business_id=business_id
    )

    if not documents:
        return "No relevant information found for this business."

    context_parts = []

    for i, document in enumerate(documents, start=1):

        file_name = document.get(
            "file_name",
            "Unknown file"
        )

        content = document.get(
            "content",
            ""
        )

        context_parts.append(
            f"""
===== DOCUMENT {i} =====
File: {file_name}

{content}
"""
        )

    return "\n".join(context_parts)