from rag_agent import answer_with_rag


question = "What are the business expenses?"

answer = answer_with_rag(question)


print("\n===== RAG ANSWER =====\n")

print(answer)

print("\n===== END ANSWER =====\n")