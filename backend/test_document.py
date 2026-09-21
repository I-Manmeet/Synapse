from document_processor import extract_text_from_txt


filename = "test.txt"

text = extract_text_from_txt(filename)

print("\n===== EXTRACTED DOCUMENT =====\n")
print(text)

print("\n===== END DOCUMENT =====\n")
