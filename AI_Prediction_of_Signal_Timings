import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import time
import os
import portalocker
import threading

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
def predict_signal_timings(vehicle_count, min_green_time=10):
    vehicle_count_scaled = scaler.transform(np.array([[vehicle_count]]))
    signal_timings = model.predict(vehicle_count_scaled)
    green_time = max(signal_timings[0][0], min_green_time)  # Ensure minimum green time
    red_time = signal_timings[0][1]  # Placeholder (adjusted based on fairness)
    yellow_time = signal_timings[0][2]
    return [green_time, red_time, yellow_time]

# Function to check if input CSV has been updated
def has_csv_updated(file_path, last_mod_time):
    try:
        current_mod_time = os.path.getmtime(file_path)
        return current_mod_time != last_mod_time, current_mod_time
    except FileNotFoundError:
        return False, last_mod_time

# Function to load CSV data, process it, and predict traffic signal timings
def process_traffic_data(input_file, output_file, last_mod_time, min_green_time=10):
    updated, last_mod_time = has_csv_updated(input_file, last_mod_time)
    
    if updated:
        try:
            # Open the input file with file locking
            with open(input_file, 'r') as f:
                portalocker.lock(f, portalocker.LockFlags.SHARED)  # Lock file for reading
                
                # Load and prepare data
                data = pd.read_csv(f)
                
            # Extract junction columns
            junction_columns = [col for col in data.columns if col.startswith('S')]
            
            if not junction_columns:
                print(f"No junction columns found in the CSV file: {input_file}")
                return last_mod_time

            vehicle_counts = data[junction_columns].values
            signal_timings = []

            # Loop over each row of the CSV to calculate signal timings for all junctions dynamically
            for i, row in data.iterrows():
                current_timings = []
                temp_timings = {}

                # Predict timings for each junction
                for junction in junction_columns:
                    if not pd.isna(row[junction]):
                        temp_timings[junction] = predict_signal_timings(row[junction], min_green_time)

                # Adjust the red light timing to be more balanced
                total_green_time = sum(temp_timings[junction][0] for junction in junction_columns if junction in temp_timings)
                total_yellow_time = sum(temp_timings[junction][2] for junction in junction_columns if junction in temp_timings)

                for junction in junction_columns:
                    if junction in temp_timings:
                        temp_timings[junction][1] = max(0, total_green_time + total_yellow_time - (temp_timings[junction][0] + temp_timings[junction][2]))

                for junction in junction_columns:
                    if junction in temp_timings:
                        current_timings.extend(temp_timings[junction])

                signal_timings.append(current_timings)

            # Dynamically create column names for the resulting DataFrame
            timing_columns = []
            for junction in junction_columns:
                timing_columns.extend([f'{junction}_Green', f'{junction}_Red', f'{junction}_Yellow'])

            # Create a DataFrame with the predicted timings
            timings_df = pd.DataFrame(signal_timings, columns=timing_columns)

            # Save the updated data to the output CSV with file locking
            with open(output_file, 'w') as f:
                portalocker.lock(f, portalocker.LockFlags.EXCLUSIVE)  # Lock file for writing
                timings_df.to_csv(f, index=False)
            print(f"Predicted signal timings saved to {output_file}")

        except FileNotFoundError:
            print(f"Error: CSV file not found. Please check the file path: {input_file}")
        except Exception as e:
            print(f"An error occurred while processing {input_file}: {e}")

    return last_mod_time

# Define the input and output CSV files for each four-road junction
input_files = [
    r"C:\Users\91934\Downloads\four_junction_1_input.csv",
    r"C:\Users\91934\Downloads\four_junction_2_input.csv",
    r"C:\Users\91934\Downloads\four_junction_3_input.csv"
]
output_files = [
    r"C:\Users\91934\Downloads\four_junction_1_signals_updated.csv",
    r"C:\Users\91934\Downloads\four_junction_2_signals_updated.csv",
    r"C:\Users\91934\Downloads\four_junction_3_signals_updated.csv"
]

# Initialize last modification times
last_mod_times = [0, 0, 0]

# Function to monitor and process each CSV file in a separate thread
def monitor_and_process(index):
    while True:
        last_mod_times[index] = process_traffic_data(input_files[index], output_files[index], last_mod_times[index], min_green_time=10)
        time.sleep(5)

# Start a thread for each junction
threads = []
for i in range(3):
    thread = threading.Thread(target=monitor_and_process, args=(i,))
    thread.start()
    threads.append(thread)

# Join threads (this will block the main thread until all threads are done)
for thread in threads:
    thread.join()
