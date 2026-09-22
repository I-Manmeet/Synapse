from rag import retrieve_context
from foundary_client import project_client


AGENT_NAME = "customer-agent"


def analyze(question: str, context: str = "", business_id: str = "") -> str:

    # Retrieve relevant information from business documents
    rag_context = retrieve_context(
    question=question,
    business_id=business_id
)

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are the Customer Agent of Synapse.

Business question:
{question}

BUSINESS CONTEXT:
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
- The BUSINESS CONTEXT was prepared specifically for the
  current business workspace.
- Use the BUSINESS CONTEXT as the authoritative baseline.
- Do not use data from another business.
- Do not substitute another time period.
- If information conflicts, explicitly report the conflict.
- Do not silently choose conflicting data.
- Do not invent customer information, reviews,
  demographics, or statistics.
- Do not treat assumptions as facts.
- Clearly distinguish information supported by business
  documents from assumptions or general knowledge.
- Clearly identify missing information.
- If the documents do not contain enough information,
  say so.
- Do not convert correlation into causation.

Return a concise customer analysis for the Manager Agent.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text