import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

# Load and prepare data
data = pd.read_csv("C:/Users/madhu/trafficS1S2S3S4.csv")
print (data)
# Dynamically get all the junction columns (assuming they are named S1, S2, ..., Sn)
junction_columns = [col for col in data.columns if col.startswith('S')]
vehicle_counts = data[junction_columns].values  # Vehicle counts for all junctions

# Sample data for training (replace this with actual data)
X_train = np.array([[10], [20], [30], [40], [50]])  # Example data
y_train = np.array([[20, 10, 5], [25, 12, 5], [30, 15, 5], [35, 18, 6], [40, 20, 7]])  # Example timings: [Green, Red, Yellow]

# Normalize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train the model
model = MLPRegressor(hidden_layer_sizes=(50, 30), max_iter=2000, learning_rate_init=0.01)
model.fit(X_train_scaled, y_train)

# Function to predict signal timings based on vehicle count
def predict_signal_timings(vehicle_count):
    vehicle_count_scaled = scaler.transform(np.array([[vehicle_count]]))
    signal_timings = model.predict(vehicle_count_scaled)
    green_time = signal_timings[0][0]
    red_time = signal_timings[0][1]  # Placeholder (we'll update red time based on the round-robin logic)
    yellow_time = 5  # Set yellow time as a constant 5 seconds
    return [green_time, red_time, yellow_time]

# Loop over each row of the CSV file to calculate signal timings for all junctions dynamically
signal_timings = []
for i, row in data.iterrows():
    current_timings = []
    
    # Step 1: Predict timings for each junction without adjusting red yet
    temp_timings = {}
    for junction in junction_columns:
        temp_timings[junction] = predict_signal_timings(row[junction])

    # Step 2: Adjust the red light timing using the round-robin approach
    for j, junction in enumerate(junction_columns):
        green_yellow_sum = 0
        
        # Sum green and yellow times of all other signals except the current one
        for other_junction in junction_columns:
            if other_junction != junction:
                green_yellow_sum += temp_timings[other_junction][0]  # Green time
                green_yellow_sum += temp_timings[other_junction][2]  # Yellow time (fixed at 5 seconds)

        # Set red time as the sum of green + yellow times of other junctions
        temp_timings[junction][1] = green_yellow_sum  # Update red time

    # Step 3: Store the updated timings for each junction in the row
    for junction in junction_columns:
        current_timings.extend(temp_timings[junction])  # Add the updated timings for the junction

    signal_timings.append(current_timings)

# Dynamically create column names for the resulting DataFrame
timing_columns = []
for junction in junction_columns:
    timing_columns.extend([f'{junction}_Green', f'{junction}_Red', f'{junction}_Yellow'])

# Create a DataFrame with the predicted timings
timings_df = pd.DataFrame(signal_timings, columns=timing_columns)

# Save the updated data to a new CSV file
timings_df.to_csv("C:/Users/madhu/traffic_signals_round_robin_updated10001.csv", index=False)

print("Predicted signal timings with round-robin logic and fixed yellow time have been saved to traffic_signals_round_robin_updated.csv")

