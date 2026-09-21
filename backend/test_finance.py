from agents.finance_agent import analyze


question = """
My clothing business sales decreased by 20%
over the last three months.
Analyze the financial situation.
"""

result = analyze(question)

print("\n===== FINANCE AGENT =====\n")
print(result)