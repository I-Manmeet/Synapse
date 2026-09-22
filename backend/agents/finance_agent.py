from foundary_client import project_client

AGENT_NAME = "finance-agent"


def analyze(question: str, context: str = "", business_id: str = "") -> str:

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are the Finance Agent of Synapse.

Business question:
{question}

BUSINESS CONTEXT:
{context}

IMPORTANT:
- The BUSINESS CONTEXT was prepared specifically for the
  current business workspace.
- Use the BUSINESS CONTEXT as the authoritative baseline.
- Use only information provided in the BUSINESS CONTEXT.
- Do not substitute another business's data.
- Do not substitute another time period.
- If information conflicts, explicitly report the conflict.
- Do not silently choose conflicting data.
- Do not invent financial values.
- Do not invent revenue, expenses, profit, margins,
  cash flow, or other financial metrics.
- If required information is missing, clearly state
  what is missing.
- Distinguish verified figures from calculations
  and interpretations.
- Do not convert correlation into causation.

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