import streamlit as st  # Import Streamlit library for building web applications
import matplotlib.pyplot as plt  # Import Matplotlib for plotting
import numpy as np  # Import NumPy for numerical computing

# Function to calculate available aircraft based on crew chiefs and maintenance
def calculate_available_aircraft(on_hands, phase_maintenance, scheduled_maintenance, unscheduled_maintenance):
    available_aircraft = on_hands - phase_maintenance - (scheduled_maintenance + unscheduled_maintenance)
    return max(0, available_aircraft)  # Ensure available aircraft is not negative

# Streamlit UI
st.title('Aircraft Availability Simulation')  # Set title of the web application

# Input fields
on_hands = st.number_input('Aircraft On-Hands', value=24)  # Input field for aircraft on hands
phase_maintenance = st.number_input('Phase Maintenance', value=4)  # Input field for phase maintenance
scheduled_maintenance = st.slider('Scheduled Maintenance per Day', 0, 10, 0)  # Slider for scheduled maintenance
unscheduled_maintenance = st.slider('Unscheduled Maintenance per Day', 0, 10, 0)  # Slider for unscheduled maintenance

# Simulation days
simulation_days = st.slider('Simulation Days', 1, 100, 60)  # Slider for simulation days

# Simulation
days = np.arange(1, simulation_days + 1)  # Array of simulation days
available_aircraft_over_time = []  # List to store available aircraft over time

for day in days:
    # Simulate stochastic nature of maintenance
    scheduled_maintenance_today = np.random.randint(0, scheduled_maintenance + 1)  # Random scheduled maintenance
    unscheduled_maintenance_today = np.random.randint(0, unscheduled_maintenance + 1)  # Random unscheduled maintenance

    # Calculate available aircraft for the day
    available_aircraft = calculate_available_aircraft(on_hands, phase_maintenance, scheduled_maintenance_today, unscheduled_maintenance_today)
    available_aircraft_over_time.append(available_aircraft)  # Append to the list

# Plot
fig, ax = plt.subplots(2, 1, figsize=(10, 12))  # Create subplots for plotting
    
# Plot aircraft availability over time
ax[0].plot(days, available_aircraft_over_time, marker='o', color='b', label='Available Aircraft')
ax[0].set_title('Aircraft Availability Over Time')
ax[0].set_xlabel('Day')
ax[0].set_ylabel('Number of Available Aircraft')
ax[0].grid(True)
ax[0].legend()

# Plot histogram for available aircraft distribution
ax[1].hist(available_aircraft_over_time, bins=10, color='skyblue', edgecolor='black')
ax[1].set_title('Distribution of Available Aircraft')
ax[1].set_xlabel('Number of Available Aircraft')
ax[1].set_ylabel('Frequency')
ax[1].grid(True)

# Display plots
st.pyplot(fig)  # Display the plots in the Streamlit app

# Summary
st.write(f"Maximum Available Aircraft: {max(available_aircraft_over_time)}")  # Display max available aircraft
st.write(f"Minimum Available Aircraft: {min(available_aircraft_over_time)}")  # Display min available aircraft
st.write(f"Average Available Aircraft: {np.mean(available_aircraft_over_time)}")  # Display average available aircraft
st.write(f"Median Available Aircraft: {np.median(available_aircraft_over_time)}")  # Display median available aircraft
