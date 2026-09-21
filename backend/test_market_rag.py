from agents.market_agent import analyze

question = "What business and market information is available in our documents?"

result = analyze(
    question,
    ""
)

print("\n===== MARKET AGENT WITH RAG =====\n")
print(result)