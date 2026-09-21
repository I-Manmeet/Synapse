from document_processor import extract_data_from_csv

df = extract_data_from_csv("test_sales.csv")

print("\n===== CSV DATA =====\n")

print(df)

print("\n===== SUMMARY =====\n")

print("Total Revenue:", df["revenue"].sum())
print("Total Quantity:", df["quantity"].sum())