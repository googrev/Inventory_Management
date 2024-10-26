import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from datetime import datetime
import joblib

# Read CSV file
df = pd.read_csv('local_store_inventory.csv')  # Make sure this matches your CSV file name

#days_since_restock: This feature calculates the number
# of days since the last restock by subtracting the last_restock_date from the current date.
# Create basic features
df['days_since_restock'] = (pd.to_datetime(datetime.now().date()) - 
                           pd.to_datetime(df['last_restock_date'])).dt.days

df['days_until_stockout'] = np.where(
    df['avg_daily_sales'] > 0,
    df['current_stock'] / df['avg_daily_sales'],
    999
)

df['needs_restock'] = (
    (df['current_stock'] < df['minimum_stock']) | 
    (df['days_until_stockout'] <= df['lead_time_days'])
).astype(int)

# Select features
features = ['current_stock', 'minimum_stock', 'maximum_stock', 
           'avg_daily_sales', 'lead_time_days', 'days_since_restock']

X = df[features]
y = df['needs_restock']

# Split and scale data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions
df['restock_probability'] = model.predict_proba(scaler.transform(X[features]))[:, 1]

# Generate alerts
alerts = df[['product_id', 'item_name', 'current_stock', 'minimum_stock', 'restock_probability']]
alerts = alerts.sort_values('restock_probability', ascending=False)

# Print alerts
print("\n=== INVENTORY ALERTS ===")
print("\nItems Needing Immediate Attention:")
print("--------------------------------")
for _, row in alerts[alerts['restock_probability'] > 0.7].iterrows():
    print(f"\nProduct: {row['item_name']} (ID: {row['product_id']})")
    print(f"Current Stock: {row['current_stock']} (Minimum: {row['minimum_stock']})")
    print(f"Restock Probability: {row['restock_probability']:.2%}")

joblib.dump(model, 'logistic_regression_model.pkl')  # Save the model
joblib.dump(scaler, 'scaler.pkl')  # Save the scaler

print("Model and scaler saved successfully!")

# Save alerts to CSV
alerts.to_csv('inventory_alerts.csv', index=False)
print("\nDetailed alerts have been saved to 'inventory_alerts.csv'")