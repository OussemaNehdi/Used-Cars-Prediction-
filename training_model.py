
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import numpy as np

# --- 1. Load the Data ---
# Read the dataset from the specified file
FILE_NAME = 'cleaned_autocentral_data.csv'
try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    print(f"Error: The file '{FILE_NAME}' was not found. Please ensure it is in the correct directory.")
    exit()

print(f"Successfully loaded {len(df)} records.")
print("\nData Head:")
print(df.head())

# --- 2. Data Cleaning and Preparation ---

# Filter out rows where the price is zero, as this is likely invalid or missing data
df = df[df['price'] > 0].copy()

# The 'brand' and 'model' columns are text (categorical), so they must be converted to numbers
# LabelEncoder is suitable for tree-based models like Random Forest
le_brand = LabelEncoder()
df['brand_encoded'] = le_brand.fit_transform(df['brand'])

le_model = LabelEncoder()
df['model_encoded'] = le_model.fit_transform(df['model'])

# Define Features (X) and Target (y)
# Exclude the original text columns and the target variable 'price'
features = ['year', 'mileage', 'cv', 'fuel_type', 'transmission', 'brand_encoded', 'model_encoded']
target = 'price'

X = df[features]
y = df[target]

# --- 3. Split the Data ---
# Split 80% for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining set size: {len(X_train)} samples")
print(f"Testing set size: {len(X_test)} samples")

# --- 4. Initialize and Train Random Forest Regressor ---
# n_estimators=100 (100 trees) is a good starting point
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
print("\nStarting model training...")

# Train the model
rf_model.fit(X_train, y_train)

print("Model training complete!")

# --- 5. Evaluate the Model ---
# Make predictions on the test set
predictions = rf_model.predict(X_test)

# Calculate metrics
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print(f"\n{'='*50}")
print(f"--- Model Performance Metrics ---")
print(f"{'='*50}")
print(f"MAE (Mean Absolute Error):  ${mae:,.2f}")
print(f"  → On average, predictions are off by ${mae:,.2f}")
print(f"\nRMSE (Root Mean Squared Error): ${rmse:,.2f}")
print(f"  → Penalizes larger errors more heavily")
print(f"\nR² Score: {r2:.4f}")
print(f"  → Model explains {r2*100:.2f}% of price variance")
if r2 > 0.8:
    print(f"  ✓ Excellent model quality!")
elif r2 > 0.6:
    print(f"  ✓ Good model quality")
elif r2 > 0.4:
    print(f"  ⚠ Moderate model quality")
else:
    print(f"  ✗ Poor model quality")
print(f"{'='*50}")

# --- Optional: Feature Importance ---
importances = pd.Series(rf_model.feature_importances_, index=X.columns)
print("\nTop 5 Feature Importances (Higher is more impactful):")
print(importances.sort_values(ascending=False).head(5))

# --- 6. Save the Model and Encoders ---
print("\n--- Saving Model and Encoders ---")

# Save the trained model
with open('car_price_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
print("✓ Model saved as 'car_price_model.pkl'")

# Save the brand encoder
with open('brand_encoder.pkl', 'wb') as f:
    pickle.dump(le_brand, f)
print("✓ Brand encoder saved as 'brand_encoder.pkl'")

# Save the model encoder
with open('model_encoder.pkl', 'wb') as f:
    pickle.dump(le_model, f)
print("✓ Model encoder saved as 'model_encoder.pkl'")

# Save the feature names for reference
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(features, f)
print("✓ Feature names saved as 'feature_names.pkl'")

print("\n✅ All files saved successfully!")
print("\nFiles created:")
print("  - car_price_model.pkl (the trained model)")
print("  - brand_encoder.pkl (for encoding brand names)")
print("  - model_encoder.pkl (for encoding model names)")
print("  - feature_names.pkl (list of features used in training)")
print("\nYou can now use these files in your FastAPI application!")