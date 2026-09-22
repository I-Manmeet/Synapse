from foundary_client import project_client
from business_context import build_business_context


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


def simulate(scenario: str, business_id: str = "") -> str:
    """What-if scenario simulator — computes before vs after for a business decision."""
    context = build_business_context(business_id)

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are the Finance Agent of Synapse, running a WHAT-IF SCENARIO SIMULATION.

BUSINESS CONTEXT (authoritative baseline — the "before" values):
{context}

SCENARIO TO SIMULATE:
{scenario}

Rules:
- Find the REAL figures in the BUSINESS CONTEXT above. For a product scenario,
  locate that product's ACTUAL price and cost from the data. Never use rounded
  or example numbers.
- All currency is Indian Rupees. Use the rupee symbol, never dollars.
- Apply the scenario change and compute the "after" values from the real
  "before" values.
- Profit margin = (price - cost) / price. Compute it from the actual price and cost.
- ALWAYS show BEFORE vs AFTER for every affected metric, with exact numbers.
- If a figure the scenario needs is missing from the context, say clearly what
  is missing instead of inventing it.
- Round money to whole rupees and percentages to one decimal place.

Return STRICT JSON only, in this shape. The angle-bracket items are placeholders —
replace them with real computed values, do NOT return them literally:
{{
  "scenario": "<restate the scenario>",
  "assumptions": ["<assumption>"],
  "results": [
    {{"metric": "<metric name>", "before": "<real value>", "after": "<real value>", "change": "<change>"}}
  ],
  "summary": "<one sentence using the real numbers>",
  "confidence": 0.0
}}
Return only the JSON, no extra text.
"""


    response = openai.responses.create(
        input=prompt
    )

    return response.output_text
