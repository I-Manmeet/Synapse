from foundary_client import project_client
from business_context import BUSINESS_CONTEXT

AGENT_NAME = "finance-agent"


def analyze(question: str, context: str = "") -> str:

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are the Finance Agent of Synapse.

Business question:
{question}

COMMON BUSINESS CONTEXT:
{BUSINESS_CONTEXT}

Additional context:
{context}

IMPORTANT:
- Use the COMMON BUSINESS CONTEXT as the authoritative baseline.
- Do not substitute another time period.
- If additional context conflicts with the common context,
  explicitly report the conflict.
- Do not silently choose conflicting data.
- Do not invent financial values.
- If required information is missing, clearly state what is missing.

Your responsibilities:

Analyze:
- Revenue
- Expenses
- Profit
- Profit margins
- Costs
- Cash flow
- Financial risks
- Financial trends

Use only the available business data.

Return a concise financial analysis for the Manager Agent.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text