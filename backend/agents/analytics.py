from foundary_client import project_client
from business_context import BUSINESS_CONTEXT

AGENT_NAME = "analytics-agent"


def analyze(question: str, context: str = "") -> str:

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are being called by the Synapse Manager Agent.

Business question:
{question}

COMMON BUSINESS CONTEXT:
{BUSINESS_CONTEXT}

Additional context:
{context}

IMPORTANT:
- Use the COMMON BUSINESS CONTEXT as the authoritative baseline.
- If additional context conflicts with the common context,
  do not silently choose one.
- Clearly report the conflict.
- Do not invent data.

Your responsibilities:

Analyze:
- Sales trends
- KPIs
- Business performance
- Measurable patterns
- Growth or decline
- Significant changes in business metrics

If information is missing, clearly state what is missing.

Return a concise analytical report for the Manager Agent.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text