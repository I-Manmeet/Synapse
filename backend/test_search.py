from search_client import search_documents


results = search_documents("Expenses")

print("\n===== SEARCH RESULTS =====\n")

for i, document in enumerate(results, start=1):

    print(f"--- Result {i} ---")

    print("File:", document["file_name"])

    print("Content:")
    print(document["content"])

    print()