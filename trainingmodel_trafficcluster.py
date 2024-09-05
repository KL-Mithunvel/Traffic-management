import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

# Load and prepare data
data = pd.read_csv("C:/Users/madhu/Downloads/traffic_with_j5.csv")
vehicle_counts = data['Vehicles'].values.reshape(-1, 1)  # Reshape for a single feature

# Sample data for training (for demonstration purposes)
# Replace this with your actual training data
X_train = np.array([[10], [20], [30], [40], [50]])  # Vehicle counts
y_train = np.array([[20, 10, 5], [25, 12, 5], [30, 15, 5], [35, 18, 6], [40, 20, 7]])  # [Green, Red, Yellow]

# Normalize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
vehicle_counts_scaled = scaler.transform(vehicle_counts)

# Train the model
model = MLPRegressor(hidden_layer_sizes=(50, 30), max_iter=2000, learning_rate_init=0.01)
model.fit(X_train_scaled, y_train)

# Function to predict signal timings based on vehicle count
def predict_signal_timings(vehicle_count):
    vehicle_count_scaled = scaler.transform(np.array([[vehicle_count]]))
    signal_timings = model.predict(vehicle_count_scaled)
    return signal_timings[0]

# Predict signal timings for each vehicle count in the CSV file
data[['Green_Time', 'Red_Time', 'Yellow_Time']] = data['Vehicles'].apply(lambda x: predict_signal_timings(x)).apply(pd.Series)

# Save the updated data to a new CSV file
data.to_csv("C:/Users/madhu/Downloads/traffic_with_j5_updated.csv", index=False)

print("Predictions have been saved to traffic_with_j5_updated.csv")
