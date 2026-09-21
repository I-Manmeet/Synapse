from document_processor import extract_text_from_docx


text = extract_text_from_docx("test_business.docx")

print("\n===== DOCX CONTENT =====\n")
print(text)

print("\n===== END DOCX =====\n")