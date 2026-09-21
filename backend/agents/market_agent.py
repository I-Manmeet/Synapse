from rag import retrieve_context
from foundary_client import project_client
from business_context import BUSINESS_CONTEXT


AGENT_NAME = "market-agent"


def analyze(question: str, context: str = "") -> str:

    # Retrieve relevant information from uploaded business documents
    rag_context = retrieve_context(question)

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are the Market Agent of Synapse.

Business question:
{question}

COMMON BUSINESS CONTEXT:
{BUSINESS_CONTEXT}

Additional context:
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
- Use the COMMON BUSINESS CONTEXT as the authoritative baseline.
- Do not substitute another time period.
- If additional context conflicts with the common context,
  explicitly report the conflict.
- Do not silently choose conflicting data.
- Do not invent competitor information, statistics, or market data.
- Use only information supported by the available data.
- Clearly distinguish business-document evidence from general market information.
- If the documents do not contain enough information, clearly state what is missing.

Return a concise market analysis for the Manager Agent.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text