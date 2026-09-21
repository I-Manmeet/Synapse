from agents.analytics import analyze


question = """
My clothing business sales decreased by 20%
over the last three months.
What should I analyze?
"""

result = analyze(question)

print("\n===== ANALYTICS AGENT =====\n")
print(result)