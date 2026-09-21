from document_processor import extract_text_from_pdf

text = extract_text_from_pdf("test_report.pdf")

print("\n===== PDF CONTENT =====\n")
print(text)

print("\n===== END PDF =====\n")