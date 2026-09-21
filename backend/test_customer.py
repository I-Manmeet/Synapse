from agents.customer_agent import analyze


question = """
My clothing business sales decreased by 20%
over the last three months.
Analyze the possible customer-related reasons.
"""

result = analyze(question)

print("\n===== CUSTOMER AGENT =====\n")
print(result)