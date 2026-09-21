from agents.market_agent import analyze


question = """
My clothing business sales decreased by 20%
over the last three months.
Analyze the possible market-related reasons.
"""

result = analyze(question)

print("\n===== MARKET AGENT =====\n")
print(result)