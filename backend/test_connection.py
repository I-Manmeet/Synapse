from foundary_client import project_client

MANAGER_AGENT = "Synapse-Manager-Agent"

openai = project_client.get_openai_client(
    agent_name=MANAGER_AGENT
)

response = openai.responses.create(
    input="""
I run a small clothing business and my sales have decreased
by 20% over the last three months.

What information should be analyzed to understand the problem?
"""
)

print("\n===== MANAGER AGENT RESPONSE =====\n")
print(response.output_text)