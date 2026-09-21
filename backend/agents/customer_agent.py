from rag import retrieve_context
from foundary_client import project_client
from business_context import BUSINESS_CONTEXT


AGENT_NAME = "customer-agent"


def analyze(question: str, context: str = "") -> str:

    # Retrieve relevant information from uploaded business documents
    rag_context = retrieve_context(question)

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are the Customer Agent of Synapse.

Business question:
{question}

COMMON BUSINESS CONTEXT:
{BUSINESS_CONTEXT}

Additional context:
{context}

RELEVANT BUSINESS DOCUMENTS:
{rag_context}

Analyze:
- Customer behavior
- Customer feedback
- Customer complaints
- Customer satisfaction
- Customer needs and preferences
- Customer segments
- Customer trends
- Retention opportunities
- Customer risks
- Customer experience opportunities

Use the retrieved documents as evidence.

IMPORTANT:
- Use the COMMON BUSINESS CONTEXT as the authoritative baseline.
- Do not substitute another time period.
- If additional context conflicts with the common context,
  explicitly report the conflict.
- Do not silently choose conflicting data.
- Do not invent customer information, reviews, demographics, or statistics.
- Do not treat assumptions as facts.
- Clearly distinguish information supported by business documents from assumptions or general knowledge.
- Clearly identify missing information.
- If the documents do not contain enough information, say so.

Return a concise customer analysis for the Manager Agent.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text