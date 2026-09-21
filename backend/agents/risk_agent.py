from foundary_client import project_client


AGENT_NAME = "risk-agent"


def assess(question: str, findings: dict) -> str:

    openai = project_client.get_openai_client(
        agent_name=AGENT_NAME
    )

    findings_text = ""

    for agent, result in findings.items():
        findings_text += f"\n\n===== {agent.upper()} =====\n"
        findings_text += str(result)

    prompt = f"""
You are the Risk Agent of Synapse.

Business question:
{question}

The following findings were produced by the specialist agents:

{findings_text}

Analyze the combined findings and identify the major business risks.

Focus on:
- financial risks
- sales/performance risks
- market risks
- customer risks
- operational risks
- dependencies
- uncertainties
- severity and potential impact

Do not invent information.

Clearly distinguish:
- evidence
- inferred risks
- missing information

Return a structured risk assessment that can be passed to the Strategy Agent.
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