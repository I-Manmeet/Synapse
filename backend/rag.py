from search_client import search_documents


def retrieve_context(
    question: str,
    top: int = 5
) -> str:
    """
    Retrieve relevant business information
    from Azure AI Search.
    """

    documents = search_documents(
        query=question,
        top=top
    )

    if not documents:
        return "No relevant information found."

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