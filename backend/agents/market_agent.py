from rag import retrieve_context
from foundary_client import project_client


AGENT_NAME = "market-agent"


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
You are the Market Agent of Synapse.

Business question:
{question}

BUSINESS CONTEXT:
{context}

RELEVANT BUSINESS DOCUMENTS:
{rag_context}

Analyze the business using:
- Market trends
- Competitors
- Customer demand
- Pricing
- Market opportunities
- Market threats
- Industry conditions
- External factors
- Seasonal factors
- Changes in market conditions

Use the retrieved documents when relevant.

IMPORTANT:
- The BUSINESS CONTEXT was prepared specifically for the
  current business workspace.
- Use the BUSINESS CONTEXT as the authoritative baseline.
- Do not use data from another business.
- Do not substitute another time period.
- If information conflicts, explicitly report the conflict.
- Do not silently choose conflicting data.
- Do not invent competitor information, statistics,
  or market data.
- Use only information supported by the available data.
- Clearly distinguish business-document evidence from
  general market information.
- Do not convert correlation into causation.
- If the documents do not contain enough information,
  clearly state what is missing.

Return a concise market analysis for the Manager Agent.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text