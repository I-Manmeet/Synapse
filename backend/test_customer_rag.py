from agents.customer_agent import analyze

question = "What are the customer and business issues mentioned in our documents?"

result = analyze(
    question,
    ""
)

print("\n===== CUSTOMER AGENT WITH RAG =====\n")
print(result)