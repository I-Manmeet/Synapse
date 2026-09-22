from foundary_client import project_client


AGENT_NAME = "risk-agent"


def assess(
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
You are the Risk Agent of Synapse.

Business ID:
{business_id}

Business question:
{question}

The following findings were produced by the specialist agents:

{findings_text}

Analyze the combined findings and identify the major
business risks for THIS business workspace.

Focus on:
- financial risks
- sales/performance risks
- market risks
- customer risks
- operational risks
- dependencies
- uncertainties
- severity and potential impact

IMPORTANT:
- Analyze only the findings provided for this business.
- Do not use information from another business.
- Do not invent information.
- Do not invent financial values, customer statistics,
  market data, or operational facts.
- Clearly distinguish evidence from inferred risks.
- Do not treat correlation as causation.
- If the evidence is insufficient, clearly say so.

Clearly distinguish:

1. Verified Evidence
2. Inference
3. Recommendation
4. Missing Information

Return a structured risk assessment that can be passed
to the Strategy Agent.
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text