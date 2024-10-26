import pandas as pd

# Load your unseen data
try:
    unseen_df = pd.read_csv('C:/Books/SEMESTER 3/hackk/unseen_Data.csv')  # Ensure this path is correct
except FileNotFoundError as e:
    print(f"Error loading unseen data: {e}")
    exit(1)

# Check the shape of the DataFrame
print("Shape of unseen data:", unseen_df.shape)

# Display the first few rows of the DataFrame
print("\nFirst few rows of unseen data:")
print(unseen_df.head())

# Check for any missing values
missing_values = unseen_df.isnull().sum()
print("\nMissing values in each column:")
print(missing_values[missing_values > 0])

# Check for any duplicate rows
duplicate_rows = unseen_df.duplicated().sum()
print("\nNumber of duplicate rows:", duplicate_rows)

# Check the number of records
num_records = len(unseen_df)
print("\nNumber of records in the unseen data:", num_records)

# Check if the DataFrame is empty
if unseen_df.empty:
    print("\nThe unseen DataFrame is empty.")
else:
    print("\nThe unseen DataFrame is not empty.")

# Print current and minimum stock values for verification
print("\nCurrent and Minimum Stock Values:")
print(unseen_df[['item_name', 'current_stock', 'minimum_stock']])

# Check for items needing immediate attention
items_needing_attention = unseen_df[unseen_df['current_stock'] <= unseen_df['minimum_stock']]

# Print the results
print("\nItems Needing Immediate Attention:")
if not items_needing_attention.empty:
    print(items_needing_attention)
    
    # Save the alerts to a CSV file
    items_needing_attention.to_csv('C:/Books/SEMESTER 3/hackk/inventory_alerts.csv', index=False)
    print("Detailed alerts have been saved to 'inventory_alerts.csv'")
else:
    print("No items need immediate attention. All items are above minimum stock levels.")
