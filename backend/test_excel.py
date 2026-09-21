from document_processor import extract_data_from_excel

df = extract_data_from_excel("test_sales.xlsx")

print("\n===== EXCEL DATA =====\n")
print(df)

print("\n===== SUMMARY =====\n")

print("Total Revenue:", df["revenue"].sum())
print("Total Quantity:", df["quantity"].sum())