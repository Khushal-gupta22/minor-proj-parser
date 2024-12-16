import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv('all_matches.csv')

# Feature Engineering
features = ['Skill_Match', 'Experience_Match', 'Location_Match', 
            'Salary_Match', 'Remote_Match', 'Degree_Match']
target = 'Total_Match_Score'  # Use Total Match as the regression target

# Check if target exists
if target not in data.columns:
    raise ValueError(f"The target column '{target}' does not exist in the dataset.")

# Handling missing data (if any)
data = data.dropna(subset=features)  # Drop rows where any feature is missing
X = data[features]
y = data[target]

# Get the full list of JobID and CandidateID
all_candidate_ids = data['CandidateID'].unique()
all_job_ids = data['JobID'].unique()

# Split into training, validation, and testing sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)  # 70% for training
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.33, random_state=42)  # 15% for validation, 15% for testing

# Initialize the XGBoost model
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)

# Define hyperparameter grid manually (for simplicity, try a few parameters)
param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1],
    'max_depth': [3, 5],
    'subsample': [0.8],
    'colsample_bytree': [0.8],
}

# Tune hyperparameters manually or use GridSearchCV alternatives
best_model = None
best_mse = float('inf')

for n_estimators in param_grid['n_estimators']:
    for learning_rate in param_grid['learning_rate']:
        for max_depth in param_grid['max_depth']:
            for subsample in param_grid['subsample']:
                for colsample_bytree in param_grid['colsample_bytree']:
                    # Create model with selected parameters
                    model = xgb.XGBRegressor(
                        n_estimators=n_estimators,
                        learning_rate=learning_rate,
                        max_depth=max_depth,
                        subsample=subsample,
                        colsample_bytree=colsample_bytree,
                        objective='reg:squarederror',
                        random_state=42
                    )

                    # Fit the model on the training data
                    model.fit(X_train, y_train)

                    # Make predictions on the validation set
                    y_val_pred = model.predict(X_val)

                    # Evaluate the model using Mean Squared Error
                    mse = mean_squared_error(y_val, y_val_pred)
                    print(f"Validation MSE: {mse:.4f}")

                    # Save the best model
                    if mse < best_mse:
                        best_mse = mse
                        best_model = model

# Make predictions on the test set using the best model
y_test_pred = best_model.predict(X_test)

# Evaluate the model using Mean Squared Error
test_mse = mean_squared_error(y_test, y_test_pred)
print(f"Test MSE: {test_mse:.4f}")

# Ensure that all CandidateID and JobID pairs are included in the output
full_mapping = pd.MultiIndex.from_product([all_candidate_ids, all_job_ids], names=["CandidateID", "JobID"]).to_frame(index=False)

# Merge predictions back into the full mapping
X_test_with_ids = data.loc[X_test.index, ['CandidateID', 'JobID']]
predictions_df = pd.DataFrame({
    'CandidateID': X_test_with_ids['CandidateID'],
    'JobID': X_test_with_ids['JobID'],
    'Actual': y_test,
    'Predicted': y_test_pred
})

# Merge full mapping with predictions to ensure each combination is present
final_output = full_mapping.merge(predictions_df, on=['CandidateID', 'JobID'], how='left')

# Fill missing predictions with the mean or a default value if needed
final_output['Predicted'].fillna(final_output['Predicted'].mean(), inplace=True)

# Save the final output to CSV
final_output.to_csv('predictions_total_match_best.csv', index=False)

# Plot Actual vs Predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_test_pred, alpha=0.7, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Match Scores')
plt.show()
