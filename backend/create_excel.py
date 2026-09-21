import pandas as pd

data = {
    "product": ["Shirt", "Jeans", "Shoes", "Jacket"],
    "revenue": [50000, 75000, 40000, 60000],
    "quantity": [100, 80, 50, 70]
}

df = pd.DataFrame(data)

df.to_excel("test_sales.xlsx", index=False)

print("Excel file created!")