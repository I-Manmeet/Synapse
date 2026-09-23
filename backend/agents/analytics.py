from foundary_client import project_client
import json

AGENT_NAME = "analytics-agent"


def analyze(question: str, context: str = "",business_id: str = ""):

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    prompt = f"""
You are being called by the Synapse Manager Agent.

Business question:
{question}

BUSINESS CONTEXT:
{context}

IMPORTANT EVIDENCE RULES:

- The BUSINESS CONTEXT was prepared specifically for the
  current business workspace.
- The user-uploaded business files are the source of truth.
- Do NOT use data from another business.
- Do NOT assume the business is Synapse Clothing.
- Do NOT use hardcoded business figures.
- Do NOT invent revenue, expenses, customers, profits,
  growth rates, or other metrics.
- Use numerical values only when they are present in the
  supplied business data or can be directly calculated from it.
- If information from different sources conflicts, clearly
  report the conflict instead of silently choosing one source.
- Do not claim causation when the data only shows correlation.
- Clearly state when required information is unavailable.
- Separate verified facts from calculations and interpretations.

Your responsibilities:

Analyze:
- Sales trends
- KPIs
- Business performance
- Measurable patterns
- Growth or decline
- Significant changes in business metrics

Focus on the user's question and use only relevant business data.

If information is missing, clearly state what is missing.

Return valid JSON only:

{
    "report": "concise analytical report",
    "kpis": {
        "revenue": null,
        "customers": null
    }
}

Use null when the information is not available.
Never invent KPI values.
Revenue and customers must come only from the supplied business data.
"""

    response = openai.responses.create(
        input=prompt
    )

    return json.loads(response.output_text)