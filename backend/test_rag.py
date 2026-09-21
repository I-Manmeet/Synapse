from rag import retrieve_context


question = "What are the business expenses?"

context = retrieve_context(question)


print("\n===== RETRIEVED CONTEXT =====\n")

print(context)

print("\n===== END CONTEXT =====\n")