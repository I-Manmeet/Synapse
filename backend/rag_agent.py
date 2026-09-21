from foundary_client import project_client
from rag import retrieve_context


AGENT_NAME = "customer-agent"


def answer_with_rag(question: str) -> str:

    context = retrieve_context(question)

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are a business assistant using retrieved business documents.

Business question:
{question}

Retrieved business information:
{context}

Instructions:

- Answer using the retrieved information.
- Do not invent facts.
- Do not use information that is not supported by the retrieved documents.
- If the documents do not contain enough information, say:
  "Insufficient information in the available documents."
- Clearly distinguish facts from assumptions.

Provide a concise answer.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text