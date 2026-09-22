from foundary_client import project_client


AGENT_NAME = "strategy-agent"


def recommend(
    question: str,
    findings: dict,
    business_id: str = ""
) -> str:

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    findings_text = ""

    for agent, result in findings.items():

        findings_text += (
            f"\n\n===== {agent.upper()} =====\n"
        )

        findings_text += str(result)

    prompt = f"""
You are the Strategy Agent of Synapse.

Business ID:
{business_id}

Business question:
{question}

The following findings were produced by the specialist
agents and Risk Agent:

{findings_text}

Develop a practical business strategy based ONLY on the
available evidence for this business.

Focus on:

- immediate actions
- short-term actions
- medium-term actions
- revenue improvement
- cost optimization
- customer retention
- operational improvement
- competitive positioning
- risk mitigation
- measurable KPIs

For every recommendation:

1. Explain the reason.
2. Identify which finding supports it.
3. Suggest a measurable KPI where possible.

IMPORTANT:
- Analyze only findings belonging to this business.
- Do not use information from another business.
- Do not invent data.
- Do not invent financial values, customer statistics,
  market data, or KPIs.
- Clearly distinguish evidence from recommendations.
- Do not treat an inference as a verified fact.
- Do not convert correlation into causation.
- If required information is missing, clearly state it.

Clearly distinguish:

1. Verified Evidence
2. Inference
3. Recommendation
4. Missing Information

Prioritize actions based on urgency and business impact.

Return a structured strategic action plan that can be passed
to the Manager Agent.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text