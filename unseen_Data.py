import pandas as pd

# Create the unseen data with consistent lengths
unseen_data = {
    'product_id': ['P027', 'P028', 'P029', 'P030', 'P031', 'P032', 'P033', 
                   'P034', 'P035', 'P036', 'P037', 'P038', 'P039', 'P040', 
                   'P041', 'P042', 'P043', 'P044'],
    'category': ['Groceries']*4 + ['Snacks']*3 + ['Beverages']*3 + ['Household']*4 + ['Stationery']*4,  # Adjusted to 18
    'item_name': ['Lentils', 'Pasta', 'Oats', 'Peas', 
                  'Popcorn', 'Cookies', 'Gummy Bears', 
                  'Energy Drink', 'Lemonade', 'Sparkling Water', 
                  'Sponges', 'Laundry Basket', 'Mop', 'Trash Bags',
                  'Markers', 'Sticky Notes', 'Highlighters', 'Stapler'],
    'current_stock': [90, 75, 110, 60, 20, 15, 9, 50, 45, 30, 
                      10, 12, 18, 5, 29, 40, 35, 8],
    'minimum_stock': [35, 30, 40, 25, 15, 12, 8, 20, 15, 10, 
                      5, 7, 5, 10, 15, 20, 20, 5],
    'maximum_stock': [115, 120, 130, 100, 80, 70, 60, 90, 75, 50, 
                      25, 40, 35, 30, 50, 80, 60, 25],
    'avg_daily_sales': [12, 10, 15, 8, 10, 5, 4, 20, 18, 7, 
                        3, 2, 1, 4, 6, 8, 7, 2],
    'lead_time_days': [3, 4, 2, 3, 3, 2, 4, 2, 3, 4, 
                       5, 3, 2, 4, 5, 4, 3, 2],
    'last_restock_date': ['2024-10-27', '2024-10-25', '2024-10-26', '2024-10-22', 
                          '2024-10-24', '2024-10-21', '2024-10-19', '2024-10-27', 
                          '2024-10-23', '2024-10-22', '2024-10-21', '2024-10-20', 
                          '2024-10-19', '2024-10-20', '2024-10-21', '2024-10-22', 
                          '2024-10-23', '2024-10-21'],
    'unit_price': [50.20, 40.75, 32.45, 54.30, 18.99, 22.99, 13.50, 
                   29.99, 25.75, 15.30, 4.99, 12.50, 20.00, 9.99, 
                   3.99, 2.50, 4.25, 11.00]
}

# Check the lengths of each list in unseen_data again
for key, value in unseen_data.items():
    print(f"Length of {key}: {len(value)}")

# Make sure all lists are of the same length
assert all(len(lst) == len(unseen_data['product_id']) for lst in unseen_data.values()), "All lists must be of the same length!"

# Create DataFrame for unseen data
unseen_df = pd.DataFrame(unseen_data)

# Save to CSV
unseen_df.to_csv('unseen_store_inventory.csv', index=False)
print("Unseen CSV file created successfully!")
