from foundary_client import project_client

AGENT_NAME = "strategy-agent"


def recommend(question: str, findings: dict) -> str:

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    findings_text = ""

    for agent, result in findings.items():
        findings_text += f"\n\n===== {agent.upper()} =====\n"
        findings_text += str(result)

    prompt = f"""
You are the Strategy Agent of Synapse.

Business question:
{question}

The following findings were produced by the specialist agents
and Risk Agent:

{findings_text}

Develop a practical business strategy based ONLY on the
available evidence.

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

Do not invent data.

Clearly distinguish:
- evidence
- recommendations
- assumptions
- missing information

Prioritize actions based on urgency and business impact.

Return a structured strategic action plan that can be passed
to the Manager Agent.
Do not treat an inference as a verified fact.
Clearly distinguish:
1. Verified evidence
2. Inference
3. Recommendation
4. Missing information
"""

    response = openai.responses.create(
        input=prompt
    )

    return response.output_text